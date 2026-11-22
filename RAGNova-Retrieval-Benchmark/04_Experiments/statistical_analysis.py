"""Cluster bootstrap and paired permutation for retrieval Hit@5 contrasts."""
import json, hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'04_Experiments'/'data'; O=ROOT/'04_Experiments'/'results'
SEED=20261114; B=5000
def norm(s):return ' '.join(s.casefold().split())
def main():
    qs={x['qid']:x for x in (json.loads(l) for l in (D/'queries_labeled.jsonl').read_text().splitlines()) if x['group_split']=='test'}
    traces=[json.loads(l) for l in (O/'per_question_traces.jsonl').read_text().splitlines()]
    titles=[]; vals=[]
    for t in traces:
        q=qs[t['qid']]; gold=q['gold_doc_id']; title=norm(q['title'])
        titles.append(title); vals.append({m:float(gold in t['rankings'][m][:5]) for m in ('bm25','rrf','rerank')})
    unique=np.array(sorted(set(titles))); grp=np.array([np.where(unique==x)[0][0] for x in titles]); rng=np.random.default_rng(SEED); out={}
    for method in ('rrf','rerank'):
        dif=np.array([v[method]-v['bm25'] for v in vals]); sums=np.bincount(grp,weights=dif,minlength=len(unique)); ns=np.bincount(grp,minlength=len(unique)); means=sums/ns
        boot=[]
        for _ in range(B):
            chosen=rng.integers(0,len(unique),len(unique));boot.append(float(sums[chosen].sum()/ns[chosen].sum()))
        observed=float(dif.mean()); signs=rng.choice([-1.,1.],size=(B,len(unique))); perm=(signs@sums)/len(vals)
        p=float((1+np.sum(np.abs(perm)>=abs(observed)))/(B+1))
        out[f'{method}_vs_bm25_hit5']={'difference':observed,'bootstrap_95ci':[float(np.percentile(boot,2.5)),float(np.percentile(boot,97.5))],'cluster_count':int(len(unique)),'question_count':len(vals),'paired_cluster_sign_flip_p_approx':p,'bootstrap_replicates':B,'seed':SEED}
    (O/'uncertainty.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
