#!/usr/bin/env python3
"""Product carbon footprint calculator.
CSV: item,stage,quantity,unit,factor,factor_unit,factor_source
Factor is kgCO2e per quantity unit.
"""
import csv, sys
from collections import defaultdict


def main():
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python calculate_pcf.py pcf.csv')
    stages=defaultdict(float); items=[]
    with open(sys.argv[1], encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            kg=float(r['quantity'])*float(r['factor'])
            stages[r['stage']]+=kg
            items.append((r['item'],r['stage'],kg,r.get('factor_source','')))
    total=sum(stages.values())
    print('Stage,kgCO2e,share')
    for stage,kg in sorted(stages.items(),key=lambda x:x[1],reverse=True):
        share=(kg/total*100) if total else 0
        print(f'{stage},{kg:.6f},{share:.2f}%')
    print(f'TOTAL,{total:.6f},100.00%')
    print('\nTop contributors:')
    for item,stage,kg,src in sorted(items,key=lambda x:x[2],reverse=True)[:10]:
        print(f'{item} | {stage} | {kg:.6f} kgCO2e | {src}')

if __name__=='__main__':
    main()
