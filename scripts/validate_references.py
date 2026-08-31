#!/usr/bin/env python3
"""Validate the reference inventory used by the China ESG skill.

The validator keeps the skill manifest and the on-disk reference directory in
lockstep.  It also enforces a minimal provenance contract: every reference
must contain at least one HTTP(S) source, and China/CCER/ETS policy snapshots
must state an explicit update baseline date.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = SCRIPT_DIR.parent

# Handles normal Markdown paths and Windows-style paths.  Reference filenames
# are intentionally limited to a single path component because the contract is
# references/*.md, not a recursive tree.
REFERENCE_PATH_RE = re.compile(
    r"references[\\/](?P<name>[^\s`<>()[\]\\/]+?\.md)(?![A-Za-z0-9_.-])",
    re.IGNORECASE,
)
HTTP_SOURCE_RE = re.compile(r"https?://[^\s<>\"`]+", re.IGNORECASE)
UPDATE_BASELINE_RE = re.compile(
    r"(?:更新基准(?:日|日期)|update\s+baseline(?:\s+date)?|last\s+updated)"
    r"\s*[:：]?\s*(?P<value>20\d{2}[-/.]\d{1,2}[-/.]\d{1,2})",
    re.IGNORECASE,
)

# Naming conventions cover the existing China-specific snapshots and remain
# extensible for parallel additions such as china-ets-2027.md or
# forestry-ccer-v02.md.  Generic framework references are not treated as
# time-sensitive merely because they mention China in explanatory prose.
DYNAMIC_NAME_RE = re.compile(
    r"^(?:china(?:[-_]|$)|ccer(?:[-_]|$)|forestry(?:[-_]|$)|"
    r"agriculture[-_]waste(?:[-_]|$))|"
    r"(?:^|[-_])(?:china|ccer|forestry|ets|emission[-_]factors|"
    r"esg[-_]regulation)(?:[-_]|$)",
    re.IGNORECASE,
)


@dataclass
class ValidationResult:
    repo_root: str
    listed_references: List[str] = field(default_factory=list)
    disk_references: List[str] = field(default_factory=list)
    missing_references: List[str] = field(default_factory=list)
    orphan_references: List[str] = field(default_factory=list)
    missing_http_sources: List[str] = field(default_factory=list)
    missing_update_baselines: List[str] = field(default_factory=list)
    invalid_update_baselines: List[str] = field(default_factory=list)
    unreadable_references: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors and not any(
            (
                self.missing_references,
                self.orphan_references,
                self.missing_http_sources,
                self.missing_update_baselines,
                self.invalid_update_baselines,
                self.unreadable_references,
            )
        )


def _resolve_path(value: Optional[Path], default: Path) -> Path:
    if value is None:
        return default.resolve()
    return value.expanduser().resolve()


def _direct_markdown_files(references_dir: Path) -> List[Path]:
    if not references_dir.is_dir():
        return []
    files = [
        path
        for path in references_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".md"
    ]
    files.sort(key=lambda path: (path.name.casefold(), path.name))
    return files


def _read_utf8(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return None


def _listed_names(skill_text: str) -> Set[str]:
    return {
        match.group("name")
        for match in REFERENCE_PATH_RE.finditer(skill_text)
    }


def _name_map(names: Iterable[str]) -> Dict[str, str]:
    """Map case-folded names to their display spelling for Windows parity."""

    result: Dict[str, str] = {}
    for name in names:
        result.setdefault(name.casefold(), name)
    return result


def _is_dynamic_reference(path: Path) -> bool:
    return bool(DYNAMIC_NAME_RE.search(path.stem))


def _valid_date(value: str) -> bool:
    normalized = value.replace("/", "-").replace(".", "-")
    try:
        date.fromisoformat(normalized)
    except ValueError:
        return False
    return True


def validate_repository(repo_root: Path) -> ValidationResult:
    repo_root = repo_root.resolve()
    result = ValidationResult(repo_root=str(repo_root))
    skill_path = repo_root / "SKILL.md"
    references_dir = repo_root / "references"

    try:
        skill_text = skill_path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        result.errors.append(f"cannot read SKILL.md: {skill_path} ({exc})")
        return result
    except UnicodeDecodeError as exc:
        result.errors.append(f"SKILL.md is not valid UTF-8: {skill_path} ({exc})")
        return result

    if not references_dir.is_dir():
        result.errors.append(f"references directory does not exist: {references_dir}")

    listed = sorted(_listed_names(skill_text), key=lambda name: (name.casefold(), name))
    disk_paths = _direct_markdown_files(references_dir)
    disk_names = [path.name for path in disk_paths]
    result.listed_references = [f"references/{name}" for name in listed]
    result.disk_references = [
        f"references/{name}" for name in disk_names
    ]

    listed_map = _name_map(listed)
    disk_map = _name_map(disk_names)

    result.missing_references = [
        f"references/{listed_map[key]}"
        for key in sorted(set(listed_map) - set(disk_map))
    ]
    result.orphan_references = [
        f"references/{disk_map[key]}"
        for key in sorted(set(disk_map) - set(listed_map))
    ]

    # Validate every on-disk reference, including an orphan, so one run gives
    # a complete remediation report.  A missing listed path has no content to
    # inspect and is already reported above.
    for path in disk_paths:
        relative_name = f"references/{path.name}"
        text = _read_utf8(path)
        if text is None:
            result.unreadable_references.append(relative_name)
            continue

        if not HTTP_SOURCE_RE.search(text):
            result.missing_http_sources.append(relative_name)

        if _is_dynamic_reference(path):
            baseline_match = UPDATE_BASELINE_RE.search(text)
            if baseline_match is None:
                result.missing_update_baselines.append(relative_name)
            elif not _valid_date(baseline_match.group("value")):
                result.invalid_update_baselines.append(
                    f"{relative_name}: {baseline_match.group('value')}"
                )

    return result


def _print_result(result: ValidationResult) -> None:
    status = "PASS" if result.ok else "FAIL"
    print(f"Reference validation: {status}")
    print(f"Repository: {result.repo_root}")
    print(f"SKILL.md references: {len(result.listed_references)}")
    print(f"On-disk references: {len(result.disk_references)}")

    if result.ok:
        print("Checks passed:")
        print("  - every SKILL.md reference exists")
        print("  - no orphan references in references/*.md")
        print("  - every reference contains an HTTP(S) source")
        print("  - every China/CCER/ETS snapshot has an update baseline date")
        return

    groups = (
        ("Errors", result.errors),
        ("Missing references", result.missing_references),
        ("Orphan references", result.orphan_references),
        ("References without HTTP(S) sources", result.missing_http_sources),
        ("Dynamic references without update baseline", result.missing_update_baselines),
        ("Dynamic references with invalid update baseline", result.invalid_update_baselines),
        ("Unreadable references", result.unreadable_references),
    )
    for title, values in groups:
        if values:
            print(f"{title}:")
            for value in values:
                print(f"  - {value}")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check the SKILL.md reference manifest and reference provenance."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="repository root (default: the parent of this scripts directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the full machine-readable result as JSON after the human summary",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    repo_root = _resolve_path(args.repo_root, DEFAULT_REPO_ROOT)
    result = validate_repository(repo_root)
    _print_result(result)
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
