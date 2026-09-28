import csv, json, os, statistics as st
T="results/tables"
def to_f(x):
    try: return float(x)
    except: return float('nan')

# --- primary FE core ---
with open(os.path.join(T,"META_DRG_axis_stouffer.csv")) as f:
    rows=list(csv.DictReader(f))
core=[x for x in rows if to_f(x['meta_FDR'])<0.05 and to_f(x['consistency'])>=0.8]
coresym={x['symbol'] for x in core}
n_fdr05=sum(1 for x in rows if to_f(x['meta_FDR'])<0.05)
print("PRIMARY FE core:",len(core),"| meta_FDR<0.05 genome-wide:",n_fdr05)

# --- RE meta ---
with open(os.path.join(T,"_R4_random_effects_meta.csv")) as f:
    re=list(csv.DictReader(f))
re_by={x['symbol']:x for x in re}
# RE core = FE core that also survive random effects (FDR_RE<0.05)
re_core=[s for s in coresym if s in re_by and to_f(re_by[s]['FDR_RE'])<0.05]
print("RE core (FE core & FDR_RE<0.05):",len(re_core),"=%.1f%%"%(100*len(re_core)/len(core)))
# RE global stats
tau2=[to_f(x['tau2']) for x in re if x['tau2'] not in ('','NA')]
i2=[to_f(x['I2']) for x in re if x['I2'] not in ('','NA')]
print("RE genome median tau2=%.3f median I2=%.1f%%  I2>50%%:%.1f%%  tau2>0:%.1f%%"%(st.median(tau2),st.median(i2),100*sum(1 for v in i2 if v>50)/len(i2),100*sum(1 for v in tau2 if v>0)/len(tau2)))

# --- 35 hubs ---
with open(os.path.join(T,"P3_hub_genes.csv")) as f:
    hubs=list(csv.DictReader(f))
hubsym=[h['symbol'] for h in hubs]
print("HUB total:",len(hubs))
in_core=[h for h in hubs if h['in_meta_core'].strip().lower() in ('yes','true','1')]
print("  in_meta_core YES:",len(in_core),"/",len(hubs))
re_sig=[h for h in hubs if h['symbol'] in re_by and to_f(re_by[h['symbol']]['FDR_RE'])<0.05]
print("  FDR_RE<0.05:",len(re_sig),"/",len(hubs),[h['symbol'] for h in re_sig])
# median I2 across 35 hubs (RE table)
hub_i2=[to_f(re_by[h]['I2']) for h in hubsym if h in re_by and re_by[h]['I2'] not in ('','NA')]
print("  median I2 across 35 hubs: %.1f%%"%(st.median(hub_i2)))

# --- gene-sets (set-level BH) ---
print("\nGENE-SETS (_R4_geneset_setlevel_bh.csv):")
with open(os.path.join(T,"_R4_geneset_setlevel_bh.csv")) as f:
    gs=list(csv.DictReader(f))
for x in gs:
    print("  %-22s scale=%-6s mean_Z=%7s stouffer_Z=%7s perm_q=%s perm_p=%s"%(x['set'],x['scale'],x['mean_Z'],x['stouffer_Z'],x['perm_q'],x['perm_p']))
# frac_up from P3_geneset_stats.csv
print("  -- frac_up (P3_geneset_stats.csv) --")
with open(os.path.join(T,"P3_geneset_stats.csv")) as f:
    gs2=list(csv.DictReader(f))
for x in gs2:
    print("  %-22s mean_Z=%7s frac_up=%s n_present=%s"%(x['set'],x['mean_Z'],x['frac_up'],x['n_present']))

# --- circular concordance (_R4_translation_noncircular.json) ---
print("\nCIRCULAR (_R4_translation_noncircular.json):")
with open(os.path.join(T,"_R4_translation_noncircular.json")) as f:
    cj=json.load(f)
for k,v in cj['strata'].items():
    print("  %-32s k=%d n=%d rate=%.4f perm_p=%.4g"%(k,v['k'],v['n'],v['rate'],v['perm_p']))

# --- bulk-only core (bulk sig, not in FE core) ---
with open(os.path.join(T,"META_bulkonly_meta.csv")) as f:
    bo={x['symbol']:x for x in csv.DictReader(f)}
bulk_sig={s for s in bo if to_f(bo[s]['meta_FDR'])<0.05}
bulk_only=bulk_sig - coresym
print("\nBULK-only significant:",len(bulk_sig),"| bulk-only NOT in FE core:",len(bulk_only),"(expect 2512)")
