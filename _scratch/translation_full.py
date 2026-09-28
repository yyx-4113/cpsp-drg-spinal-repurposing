import csv, os, math
T="results/tables"
def to_f(x):
    try: return float(x)
    except: return float('nan')
def sgn(x):
    return 1 if x>0 else (-1 if x<0 else 0)
def wilson(k,n):
    if n==0: return (0,0)
    p=k/n; z=1.96
    den=1+z*z/n
    c=(p+z*z/(2*n))/den
    h=(z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)))/den
    return (100*(c-h),100*(c+h))

st={}
with open(os.path.join(T,"META_DRG_axis_stouffer.csv")) as f:
    for r in csv.DictReader(f):
        st[r['symbol']]={'meta_Z':to_f(r['meta_Z']),'meta_FDR':to_f(r['meta_FDR']),
                         'consistency':to_f(r['consistency']),'incision_lfc':to_f(r['incision_lfc'])}
ni={}
with open(os.path.join(T,"_R4_nerveinjury_only_meta.csv")) as f:
    for r in csv.DictReader(f):
        ni[r['symbol']]={'Z_NI':to_f(r['Z_NI']),'FDR_NI':to_f(r['FDR_NI']),
                         'ni_cons':to_f(r['ni_consistency']),'incision_Z':to_f(r['incision_Z'])}

# (c) "53.8% (2,318/4,306)": among genes with ni_consistency>=0.8 that have incision, six-input meta vs incision
n=ag=0
for s in ni:
    if ni[s]['ni_cons']>=0.8 and s in st and sgn(st[s]['incision_lfc']):
        n+=1
        if sgn(st[s]['meta_Z'])==sgn(st[s]['incision_lfc']): ag+=1
print("NI-consistency>=0.8 (six-input meta vs incision): agree=%d n=%d rate=%.4f CI=%.1f-%.1f"%(ag,n,ag/n,*wilson(ag,n)))

# overall circular CI
ov_n=ov_ag=0
for s,d in st.items():
    if sgn(d['meta_Z']) and sgn(d['incision_lfc']):
        ov_n+=1
        if sgn(d['meta_Z'])==sgn(d['incision_lfc']): ov_ag+=1
print("OVERALL circular: %d/%d=%.4f CI=%.1f-%.1f"%(ov_ag,ov_n,ov_ag/ov_n,*wilson(ov_ag,ov_n)))

# core-restricted circular CI
core=[s for s,d in st.items() if d['meta_FDR']<0.05 and d['consistency']>=0.8]
cr_n=cr_ag=0
for s in core:
    d=st[s]
    if sgn(d['incision_lfc']):
        cr_n+=1
        if sgn(d['meta_Z'])==sgn(d['incision_lfc']): cr_ag+=1
print("CORE-restricted circular: %d/%d=%.4f CI=%.1f-%.1f"%(cr_ag,cr_n,cr_ag/cr_n,*wilson(cr_ag,cr_n)))

# NI-only meta (Z_NI) vs incision, strong stratum (NI_FDR05 & NIcons>=0.8)
sn=sag=0
for s,d in ni.items():
    if d['FDR_NI']<0.05 and d['ni_cons']>=0.8 and sgn(d['incision_Z']):
        sn+=1
        if sgn(d['Z_NI'])==sgn(d['incision_Z']): sag+=1
print("NI-strong stratum (Z_NI vs incision): %d/%d=%.4f CI=%.1f-%.1f"%(sag,sn,sag/sn,*wilson(sag,sn)))
# NI-only meta vs incision, ALL genes (background)
bn=bag=0
for s,d in ni.items():
    if sgn(d['incision_Z']):
        bn+=1
        if sgn(d['Z_NI'])==sgn(d['incision_Z']): bag+=1
print("NI background (Z_NI vs incision): %d/%d=%.4f"%(bag,bn,bag/bn))
