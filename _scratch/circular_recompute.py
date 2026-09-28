import csv, os
T="results/tables"
def to_f(x):
    try: return float(x)
    except: return float('nan')
def sgn(x):
    if x>0: return 1
    if x<0: return -1
    return 0
rows={}
with open(os.path.join(T,"META_DRG_axis_stouffer.csv")) as f:
    for r in csv.DictReader(f):
        rows[r['symbol']]={'meta_Z':to_f(r['meta_Z']),'meta_FDR':to_f(r['meta_FDR']),
                            'consistency':to_f(r['consistency']),'incision_lfc':to_f(r['incision_lfc'])}
# overall circular: sign(meta_Z)==sign(incision_lfc) over genes with both nonzero
ov_n=ov_ag=0
for s,d in rows.items():
    if sgn(d['meta_Z']) and sgn(d['incision_lfc']):
        ov_n+=1
        if sgn(d['meta_Z'])==sgn(d['incision_lfc']): ov_ag+=1
print("OVERALL circular: agree=%d n=%d rate=%.4f"%(ov_ag,ov_n,ov_ag/ov_n))
# core-restricted: primary core (meta_FDR<0.05 & consistency>=0.8) with incision
core=[s for s,d in rows.items() if d['meta_FDR']<0.05 and d['consistency']>=0.8]
cr_n=cr_ag=0
for s in core:
    d=rows[s]
    if sgn(d['incision_lfc']):
        cr_n+=1
        if sgn(d['meta_Z'])==sgn(d['incision_lfc']): cr_ag+=1
print("CORE-restricted circular: agree=%d n=%d rate=%.4f"%(cr_ag,cr_n,cr_ag/cr_n if cr_n else 0))
print("primary core size:",len(core))
