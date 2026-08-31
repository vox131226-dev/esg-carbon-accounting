---
name: china-esg-carbon-accounting
description: 中国化ESG、组织温室气体盘查、产品碳足迹、LCA、Scope 1/2/3、中国碳市场CEA/CCER与可持续发展报告编制统一技能。适用于企业碳盘查、产品碳足迹、供应链碳核算、ESG报告、碳资产管理、碳市场项目评估与尽职调查。
---

# China ESG & Carbon Accounting

## 目标

对企业、产品、项目和供应链开展结构化ESG与碳核算分析，并输出可审阅、可追溯、可复核的计算结果、底稿和正式报告。

## 核心框架

优先按以下框架组织工作，并在具体项目中核验最新有效版本：

- GHG Protocol Corporate Standard
- GHG Protocol Scope 2 Guidance
- GHG Protocol Scope 3 Standard
- ISO 14064-1
- ISO 14067
- ISO 14040 / ISO 14044
- IFRS S1 / IFRS S2
- GRI Standards
- 中国境内证券交易所可持续发展报告相关规则
- 中国生态环境主管部门企业温室气体核算与报告规则
- 全国碳排放权交易市场相关规则
- 全国温室气体自愿减排交易市场与CCER相关规则、方法学和登记交易要求

## 路由

根据用户任务自动进入以下模块：

1. `corporate-ghg-inventory`
   组织温室气体盘查、Scope 1/2/3、基准年、组织边界、运营边界、排放因子、数据质量、不确定性。

2. `product-carbon-footprint`
   产品碳足迹、ISO 14067、LCA、功能单位、系统边界、BOM、运输、能源、包装、废弃阶段、分配与截断规则。

3. `esg-report-writer`
   ESG/可持续发展报告、议题识别、指标映射、数据缺口、温室气体章节、气候相关风险与机会、治理与目标。

4. `china-carbon-market`
   CEA、CCER、履约、配额、碳资产、减排项目识别、方法学适用性、项目可行性、开发风险与尽职调查。

## 路由与必读资料

| 路由 | 必读资料 | 中国项目或专项资料 |
|---|---|---|
| `corporate-ghg-inventory` | `references/corporate-ghg.md`、`references/data-quality-and-audit.md` | 中国因子任务读取 `references/china-emission-factors.md` |
| `product-carbon-footprint` | `references/product-carbon-footprint.md`、`references/data-quality-and-audit.md` | 中国产品读取 `references/china-product-carbon-footprint.md` 和 `references/china-emission-factors.md` |
| `esg-report-writer` | `references/esg-reporting.md`、`references/data-quality-and-audit.md` | 中国企业读取 `references/china-esg-regulation-2026.md` 和 `references/china-sustainability-disclosure-2026.md` |
| `china-carbon-market` | `references/china-carbon-market.md`、`references/data-quality-and-audit.md` | 按CEA、CCER、林业、农业废弃物或地热项目读取对应中国专项资料 |

只加载与当前任务有关的专项reference，不因知识包中存在某份文件就把其规则套用到无关任务。

## 中国规则时效检查（强制）

处理中国项目时，在形成正式结论前必须检查规则状态：

1. 区分“正式有效”“已修订”“已废止”“征求意见稿”“编制说明”“专家解读”。
2. 征求意见稿只能用于储备项目和政策趋势分析，不能作为正式登记、核证、披露或认证依据。
3. CCER项目先查看 `references/ccer-current-methodologies-2026.md`，再进入对应专项reference。
4. 林业项目必须同时查看 `references/forestry-ccer-2026.md`。
5. 猪场粪污或农业废弃物项目必须查看 `references/agriculture-waste-ccer.md`。
6. 中深层地热能供暖项目必须查看 `references/geothermal-ccer-2026.md`。
7. 全国碳市场项目必须查看 `references/china-ets-2026.md`。
8. 排放因子选择必须查看 `references/china-emission-factors.md`，并区分产品碳足迹、企业Scope 2、全国碳市场和CCER四类用途。
9. 中国上市公司ESG报告必须查看 `references/china-esg-regulation-2026.md`。
10. 中国企业气候披露或可持续信息鉴证任务必须查看 `references/china-sustainability-disclosure-2026.md`。
11. 产品碳足迹任务必须查看 `references/china-product-carbon-footprint.md`。
12. reference中的日期是知识快照；正式业务仍需核验生态环境部、交易所及其他主管部门是否已有更新。

## 强制工作流

### 第一步：明确任务与边界

必须识别：
- 核算对象
- 报告期或生命周期阶段
- 组织边界或产品系统边界
- 地理边界
- 数据完整性
- 是否用于内部管理、披露、核查、认证、交易、融资或政府报送

若用户资料不完整，不得伪造关键活动数据、排放因子或政策结论。可采用情景假设，但必须单独标注。

### 第二步：建立数据清单

组织碳盘查至少检查：
- 固定燃烧
- 移动燃烧
- 工艺排放
- 逸散排放
- 外购电力、热力、蒸汽、冷量
- Scope 3十五类相关活动

产品碳足迹至少检查：
- 原材料与BOM
- 上游加工
- 上游运输
- 制造能源
- 辅料与耗材
- 包装
- 仓储与下游运输
- 使用阶段
- 报废、回收和处置

### 第三步：因子选择

排放因子遵循优先级：
1. 项目用途所适用的中国强制监管规则、核算指南或方法学参数
2. 国家温室气体排放因子数据库最新版和中国主管部门官方因子
3. 产品规则、行业标准、经认可数据库或供应商实测数据
4. IPCC、DEFRA、EPA、Ember、EXIOBASE 等国际来源
5. 支出法或其他估算法，仅在更高质量数据不可得时使用

所有因子必须记录：来源、年份、地域、单位、适用边界、是否含CH4/N2O、GWP版本。

不得混用以下口径：
- 产品碳足迹电力因子
- 企业组织层面Scope 2因子
- 全国碳市场监管核算参数
- CCER方法学参数或基准线因子

### 第四步：计算

基本公式：

`排放量 = 活动数据 × 排放因子 × 必要的单位换算或氧化/转化参数`

CO2e统一换算：

`CO2e = Σ(温室气体质量 × 对应GWP)`

禁止在没有说明的情况下混用不同GWP版本。

### 第五步：质量控制

至少执行：
- 单位一致性检查
- 数量级检查
- 时间边界检查
- 重复计算检查
- Scope归类检查
- 因子地域适用性检查
- 因子用途适用性检查
- 缺失数据检查
- 异常值检查
- 关键排放源Top 5复核

### 第六步：输出

默认至少输出：
- 核算边界
- 数据与假设
- 排放因子来源
- Scope或生命周期阶段结果
- 总排放量
- 排放热点
- 数据质量与局限性
- 减排机会
- 可核查底稿字段清单

## ESG报告规则

编制ESG或可持续发展报告时：
- 先做适用规则识别，再写正文
- 区分强制披露、建议披露、自愿披露
- 不得把缺少证据的数据写成确定事实
- 对气候指标重点检查Scope 1、Scope 2、重大Scope 3、目标、基准年、减排进展、气候风险与机会、治理和财务影响
- 对中国上市公司任务，优先核验交易所最新规则和行业适用性
- 目标、承诺、规划、已完成业绩必须分开表述

## 中国碳市场规则

处理CEA/CCER时必须区分：
- 强制碳市场配额资产
- 自愿减排量资产
- 项目减排量预测
- 已登记项目
- 已核证/已登记减排量
- 已交易或已注销资产

CCER项目评估必须核验：
- 方法学正式有效状态
- 方法学适用条件
- 项目边界
- 额外性
- 基准线
- 监测计划
- 计入期
- 权属
- 重复计算/重复申报风险
- 审定与核查可实施性
- 登记交易约束
- 收益分配和合同约束

## 尽职调查模式

若用户询问“项目能不能接”“是否可开发”“风险在哪里”，按以下顺序：
1. 法律与权属
2. 方法学适用性和正式有效状态
3. 技术可开发性
4. 数据可得性
5. 历史行为与追溯问题
6. 环评/能评/林权/用地/许可等合规
7. 是否存在重复开发或第三方权利
8. 预估减排量及敏感性
9. 开发成本与交易成本
10. 合同和退出机制

结论分为：
- 可接受
- 有条件接受
- 暂缓
- 不建议接受

并明确列出前置条件。

## 参考文件

基础规则：
- `references/corporate-ghg.md`
- `references/product-carbon-footprint.md`
- `references/esg-reporting.md`
- `references/china-carbon-market.md`
- `references/data-quality-and-audit.md`

中国化增强：
- `references/ccer-current-methodologies-2026.md`
- `references/forestry-ccer-2026.md`
- `references/agriculture-waste-ccer.md`
- `references/geothermal-ccer-2026.md`
- `references/china-ets-2026.md`
- `references/china-emission-factors.md`
- `references/china-product-carbon-footprint.md`
- `references/china-esg-regulation-2026.md`
- `references/china-sustainability-disclosure-2026.md`

计算工具：
- `scripts/calculate_ghg.py`
- `scripts/calculate_pcf.py`

知识维护工具：
- `scripts/validate_references.py`
- `scripts/build_gpt_knowledge.py`

## 知识维护与发布

更新政策、方法学、排放因子或监管规则时：

1. 只把主管部门、交易所、标准发布机构等一手来源作为效力状态依据。
2. 记录发布机构、文件编号、发布日期、生效日期、效力状态、官方链接和最后核验日期。
3. 正式版、征求意见稿、编制说明和解读必须分别标注；新文件替代旧文件时明确废止或替代关系。
4. 运行 `scripts/validate_references.py`，检查SKILL路由、孤立reference、来源链接和基准日期。
5. 运行 `scripts/build_gpt_knowledge.py`，重新生成可上传到自定义GPT的知识包。
6. 在企业碳盘查、产品碳足迹、ESG报告、CEA、CCER五类任务上执行回归测试后再发布。

## 最重要的原则

1. 项目用途所适用的中国强制规则优先于通用国外默认规则。
2. 当前政策、交易规则、方法学和电力排放因子属于时效性信息，正式项目必须核验最新版。
3. 征求意见稿不能当作正式业务依据。
4. 计算过程必须可以从结果追溯到活动数据和因子。
5. 不确定性、估算值、缺失值必须显式标注。
6. 任何拟用于第三方核查、认证、政府报送、交易或公开披露的结果，都要保留完整底稿和证据链。
