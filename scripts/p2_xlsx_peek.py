#!/usr/bin/env python3
# p2_xlsx_peek.py -- full structure of GSE265957 xlsx (sheets, shapes, columns, head)
import os, pandas as pd
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
P=os.path.join(ROOT,"data/raw/GSE265957/GSE265957_processed_files_tpms_and_degs_SNI_TRAP_and_RF.xlsx")
xl=pd.ExcelFile(P)
print("TOTAL SHEETS:",len(xl.sheet_names))
for s in xl.sheet_names:
    df=xl.parse(s, nrows=4)
    print("="*70)
    print(f"[SHEET] {s}  shape_head={df.shape}  ncols={len(df.columns)}")
    print("  cols[:12]:",[str(c) for c in df.columns[:12]])
    if len(df.columns)>12:
        print("  cols[12:]:",[str(c) for c in df.columns[12:24]])
