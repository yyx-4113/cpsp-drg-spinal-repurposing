import csv, json, os
T="results/tables"
def to_f(x):
    try: return float(x)
    except: return float('nan')

with open(os.path.join(T,"META_DRG_axis_stouffer.csv")) as f:
    r=list(csv.DictReader(f))
core=[x for x in r if to_f(x['meta_FDR'])<0.05 and to_f(x['consistency'])>=0.8]
coresym={x['symbol'] for x in core}
print("PRIMARY FE core:",len(core))

with open(os.path.join(T,"META_bulkonly_meta.csv")) as f:
    rb={x['symbol']:x for x in csv.DictReader(f)}

def bulk_fdr(s): return to_f(rb[s]['meta_FDR']) if s in rb else float('nan')
def bulk_cons(s): return to_f(rb[s]['consistency']) if s in rb else float('nan')
def bulk_K(s): return int(rb[s]['K']) if s in rb else 0

strict=[s for s in coresym if s in rb and bulk_fdr(s)<0.05 and bulk_cons(s)>=0.8]
relaxed=[s for s in coresym if s in rb and bulk_fdr(s)<0.05 and bulk_cons(s)>=0.75]
strict_K={}; 
for s in strict: strict_K[bulk_K(s)]=strict_K.get(bulk_K(s),0)+1
relaxed_K={}
for s in relaxed: relaxed_K[bulk_K(s)]=relaxed_K.get(bulk_K(s),0)+1
print("bulk strict(>=0.8):",len(strict),"=%.1f%%"%(100*len(strict)/len(core)),"K dist",strict_K)
print("bulk relaxed(>=0.75):",len(relaxed),"=%.1f%%"%(100*len(relaxed)/len(core)),"K dist",relaxed_K)
pure44=sum(1 for s in strict if bulk_K(s)==4)
print("pure 4/4 (K=4 within strict):",pure44,"=%.1f%%"%(100*pure44/len(core)))
outside=len(coresym)-len(relaxed)
print("outside even relaxed:",outside)
absent=sum(1 for s in coresym if s not in rb)
nonsig=sum(1 for s in coresym if s in rb and bulk_fdr(s)>=0.05)
print("core lacking bulk support: absent",absent,"+ nonsig",nonsig,"=",absent+nonsig)

# CACNA2D1 from primary stouffer
c={x['symbol']:x for x in r}.get('CACNA2D1')
print("\nCACNA2D1 primary:",{k:c[k] for k in ('meta_Z','meta_FDR','consistency','n_up','n_dn','K')} if c else 'MISSING')
if c:
    lfcs={k[4:]:c[k] for k in c if k.startswith('lfc')}
    print("  lfcs:",lfcs)

# translation json
with open(os.path.join(T,"_R4_nerveinjury_only_summary.json")) as f:
    j=json.load(f)
print("\nTRANSLATION strata:")
for k,v in j.items():
    print(k,"=",v)
