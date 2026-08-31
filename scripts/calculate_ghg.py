#!/usr/bin/env python3
"""Simple auditable GHG calculator.
Input CSV columns: source,scope,category,activity,unit,factor,factor_unit,factor_source
Factor must be expressed as kgCO2e per activity unit.
"""
import csv, sys
from collections import defaultdict


def calculate(path):
    rows=[]; totals=defaultdict(float)
    with open(path, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            activity=float(r['activity'])
            factor=float(r['factor'])
            kg=activity*factor
            r['emissions_kgco2e']=kg
            r['emissions_tco2e']=kg/1000
            totals[r['scope']]+=kg
            rows.append(r)
    return rows, totals


def main():
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python calculate_ghg.py inventory.csv')
    rows, totals=calculate(sys.argv[1])
    print('Scope,tCO2e')
    for scope,kg in sorted(totals.items()):
        print(f'{scope},{kg/1000:.6f}')
    print(f'TOTAL,{sum(totals.values())/1000:.6f}')
    print('\nSource detail:')
    for r in sorted(rows,key=lambda x:x['emissions_kgco2e'],reverse=True):
        print(f"{r['source']}: {r['emissions_tco2e']:.6f} tCO2e")

if __name__=='__main__':
    main()
