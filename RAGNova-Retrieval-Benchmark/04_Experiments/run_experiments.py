"""Reproducible sparse retrieval and binary reader experiments for BoolQ."""
from __future__ import annotations
import json, re, time, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import joblib

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'04_Experiments'/'data'; OUT=ROOT/'04_Experiments'/'results'; OUT.mkdir(exist_ok=True)
SEED=20261114
def readj(path): return [json.loads(x) for x in path.read_text(encoding='utf8').splitlines() if x]
def tokens(s): return re.findall(r"(?u)\b\w+\b",s.casefold())
def percentile_latency(func, arr, reps=300):
    times=[]
    for x in arr[:reps]:
        t=time.perf_counter();func(x);times.append((time.perf_counter()-t)*1000)
    return {"p50_ms":float(np.percentile(times,50)),"p95_ms":float(np.percentile(times,95)),"n":len(times)}
def rankings(scores,k=10): return np.argpartition(-scores,k-1)[:k][np.argsort(-scores[np.argpartition(-scores,k-1)[:k]])]
def mrr_at(ranked,gold):
    for i,d in enumerate(ranked,1):
        if d==gold:return 1/i
    return 0.
def metrics(rows, score_name, docids):
    hit={k:[] for k in (1,5,10)}; mrr=[]; ndcg=[]
    for r in rows:
        s=r[score_name]; order=rankings(s,10); gold=r['gold']
        for k in hit: hit[k].append(float(gold in order[:k]))
        mrr.append(mrr_at(order,gold)); ndcg.append(1/np.log2(np.where(order==gold)[0][0]+2) if gold in order else 0.)
    return {f'Hit@{k}':float(np.mean(v)) for k,v in hit.items()}|{'MRR@10':float(np.mean(mrr)),'nDCG@10':float(np.mean(ndcg)),'n':len(rows)}
def main():
    print('loading data',flush=True)
    q=readj(DATA/'queries_labeled.jsonl'); docs=readj(DATA/'documents.jsonl'); texts=[d['text'] for d in docs]; ids=[d['doc_id'] for d in docs]; id2idx={x:i for i,x in enumerate(ids)}
    train=[x for x in q if x['group_split']=='train']; val=[x for x in q if x['group_split']=='validation']; test=[x for x in q if x['group_split']=='test']
    # Fit corpus representations using the public document corpus; labels and answers are excluded.
    tv=TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=60000,sublinear_tf=True,dtype=np.float32)
    D=tv.fit_transform(texts); cv=CountVectorizer(min_df=2,max_features=60000,dtype=np.float32); C=cv.fit_transform(texts)
    print('sparse vectorization complete',D.shape,C.shape,flush=True)
    df=np.asarray((C>0).sum(axis=0)).ravel().astype(np.float32); avgdl=float(np.asarray(C.sum(axis=1)).mean()); lengths=np.asarray(C.sum(axis=1)).ravel().astype(np.float32)
    # BM25 postings are computed only for query terms, avoiding a dense query-document matrix.
    idf=np.log(1+(len(texts)-df+0.5)/(df+0.5)).astype(np.float32)
    def bm25_one(query):
        qv=cv.transform([query]); terms=qv.indices; vals=np.zeros(len(texts),np.float32)
        for t in terms:
            col=C[:,t].tocoo(); tf=col.data
            den=tf+1.5*(1-0.75+0.75*lengths[col.row]/avgdl)
            vals[col.row]+=idf[t]*(tf*(1.5+1))/(den+1e-9)
        return vals
    def tf_one(query):return (D@tv.transform([query]).T).toarray().ravel()
    # LSA document/query embedding trained on document texts only.
    svd=TruncatedSVD(n_components=48,random_state=SEED,n_iter=3); Zd=normalize(svd.fit_transform(D).astype(np.float32))
    print('LSA complete',flush=True)
    def lsa_one(query):return (Zd@normalize(svd.transform(tv.transform([query])).astype(np.float32)).T).ravel()
    val_rows=[]; print('validation scoring',flush=True)
    for x in val:
        val_rows.append({'gold':id2idx[x['gold_doc_id']],'bm25':bm25_one(x['question']),'tfidf':tf_one(x['question']),'lsa':lsa_one(x['question'])})
    # Tune convex BM25 / TF-IDF fusion only on validation.
    alphas=np.linspace(0,1,11); tuning=[]
    for a in alphas:
        sc=[a*r['bm25']/(r['bm25'].max()+1e-9)+(1-a)*r['tfidf']/(r['tfidf'].max()+1e-9) for r in val_rows]
        tuning.append((float(np.mean([r['gold'] in rankings(s,5) for r,s in zip(val_rows,sc)])),float(a)))
    alpha=max(tuning)[1]
    print('validation complete; alpha',alpha,flush=True)
    # Train logistic reranker on train-query retrieval candidates with hard negatives.
    # Features are normalized BM25, TF-IDF, LSA, and title overlap, with no answer labels.
    rer_X=[]; rer_y=[]
    rng=np.random.default_rng(SEED); fit_train=sorted(rng.choice(len(train),size=min(1600,len(train)),replace=False))
    for ix in fit_train:
        x=train[ix]
        b=bm25_one(x['question']); t=tf_one(x['question']); l=lsa_one(x['question']); gold=id2idx[x['gold_doc_id']]
        cand=np.unique(np.r_[rankings(b,8),rankings(t,8),rankings(l,8),gold])
        qt=set(tokens(x['question']))
        for j in cand:
            ov=len(qt & set(tokens(docs[j]['title'])))/max(1,len(qt))
            rer_X.append([b[j]/(b.max()+1e-9),t[j]/(t.max()+1e-9),l[j],ov]); rer_y.append(int(j==gold))
    print('reranker features ready',len(rer_y),flush=True)
    rer=LogisticRegression(max_iter=500,class_weight='balanced',random_state=SEED).fit(np.asarray(rer_X),np.asarray(rer_y))
    # Binary decision reader learns from the training question + gold passage only.
    reader=make_pipeline(TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=60000,sublinear_tf=True),LogisticRegression(max_iter=300,class_weight='balanced',random_state=SEED))
    reader.fit([x['question']+' [SEP] '+texts[id2idx[x['gold_doc_id']]] for x in train],[int(x['answer']) for x in train]); print('reader fit complete',flush=True)
    # Freeze hyperparameters, then evaluate once on held-out titles.
    rows=[]; pred=[]; actual=[]; trace=[]; lat=[]
    for x in test:
        t0=time.perf_counter(); b=bm25_one(x['question']); t=tf_one(x['question']); l=lsa_one(x['question'])
        hybrid=alpha*b/(b.max()+1e-9)+(1-alpha)*t/(t.max()+1e-9)
        # RRF uses top-100 lists, fixed k=60.
        rrf=np.zeros(len(docs),np.float32)
        for arr in (b,t,l):
            for rank,j in enumerate(rankings(arr,100),1):rrf[j]+=1/(60+rank)
        cand=np.unique(np.r_[rankings(rrf,30),rankings(b,30),rankings(t,30),rankings(l,30)])
        qtok=set(tokens(x['question'])); feats=[]
        for j in cand:
            ov=len(qtok & set(tokens(docs[j]['title'])))/max(1,len(qtok))
            feats.append([b[j]/(b.max()+1e-9),t[j]/(t.max()+1e-9),l[j],ov])
        rs=rer.predict_proba(np.asarray(feats))[:,1]; rscore=np.full(len(docs),-1.,np.float32); rscore[cand]=rs
        pred_doc=int(np.argmax(rscore)); inp=x['question']+' [SEP] '+texts[pred_doc]; pp=float(reader.predict_proba([inp])[0,1]); yhat=int(pp>=0.5)
        rows.append({'gold':id2idx[x['gold_doc_id']],'bm25':b,'tfidf':t,'lsa':l,'hybrid':hybrid,'rrf':rrf,'rerank':rscore})
        pred.append(yhat);actual.append(int(x['answer'])); lat.append((time.perf_counter()-t0)*1000)
        orders={key:rankings(rows[-1][key],10) for key in ('bm25','tfidf','lsa','hybrid','rrf','rerank')}
        trace.append({'qid':x['qid'],'question':x['question'],'answer':bool(x['answer']),'prediction':bool(yhat),'answer_probability_yes':pp,'retrieved_doc_id':ids[pred_doc],'retrieved_title':docs[pred_doc]['title'],'gold_doc_id':x['gold_doc_id'],'rankings':{k:[ids[int(j)] for j in v] for k,v in orders.items()},'top_context':texts[pred_doc]})
    print('test scoring complete',flush=True)
    result={name:metrics(rows,name,ids) for name in ('bm25','tfidf','lsa','hybrid','rrf','rerank')}
    pr,rc,f1,_=precision_recall_fscore_support(actual,pred,average='binary',zero_division=0)
    result['reader_top_reranked_context']={'accuracy':float(accuracy_score(actual,pred)),'precision_yes':float(pr),'recall_yes':float(rc),'f1_yes':float(f1),'n':len(test)}
    result['latency_e2e_ms']={'p50':float(np.percentile(lat,50)),'p95':float(np.percentile(lat,95)),'mean':float(np.mean(lat)),'n':len(lat),'scope':'CPU; retrieval + reranking + binary reader; corpus representations already loaded'}
    result['settings']={'seed':SEED,'documents':len(docs),'train_queries':len(train),'reranker_fit_queries':len(fit_train),'validation_queries':len(val),'test_queries':len(test),'fusion_alpha_bm25':alpha,'fusion_alpha_selected_on':'validation Hit@5','rrf_k':60,'svd_components':48,'reranker':'balanced logistic regression on retrieval features, fitted on fixed 1,600-query training sample','reader':'TF-IDF + logistic regression binary yes/no','answers_are_generative':False,'evaluation':'title-group holdout; all labeled test predictions scored once'}
    (OUT/'metrics.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    (OUT/'per_question_traces.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in trace)+'\n',encoding='utf8')
    pd.DataFrame([{**{'method':k},**v} for k,v in result.items() if isinstance(v,dict) and 'Hit@1' in v]).to_csv(OUT/'retrieval_metrics.csv',index=False)
    pd.DataFrame([{'alpha_bm25':a,'validation_hit5':s} for s,a in tuning]).to_csv(OUT/'validation_fusion_tuning.csv',index=False)
    joblib.dump({'tfidf':tv,'count':cv,'count_matrix':C,'svd':svd,'doc_tfidf':D,'doc_lsa':Zd,'docs':docs,'bm25_idf':idf,'doc_lengths':lengths,'avgdl':avgdl,'reranker':rer,'reader':reader,'fusion_alpha':alpha},OUT/'rag_nova_models.joblib',compress=3)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
