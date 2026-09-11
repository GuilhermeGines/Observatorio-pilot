import hashlib
import json
from . import db

def bundles(documents):
    return {country:[d for d in documents if d['country']==country] for country in dict.fromkeys(d['country'] for d in documents)}

def key(documents,config,prompt):
    return hashlib.sha256(db.dumps({'documents':sorted(documents,key=lambda d:d['revision_id']),
        'model':config['model'],'provider':config['provider'],'language':config['language_policy'],
        'keyword':config.get('summary_keyword',''),'topics':config.get('summary_topics',[]),'prompt':prompt}).encode()).hexdigest()

def load(documents,config,prompt):
    cached=[];missing=[]
    with db.connect() as connection:
        for country,docs in bundles(documents).items():
            row=connection.execute('SELECT value FROM summary_cache WHERE key=?',(key(docs,config,prompt),)).fetchone()
            if row: cached.extend(json.loads(row['value']))
            else: missing.extend(docs)
    return cached,missing

def save(documents,summaries,config,prompt):
    with db.connect() as connection:
        for country,docs in bundles(documents).items():
            items=[s.model_dump() for s in summaries if s.country==country]
            if items: connection.execute('INSERT OR REPLACE INTO summary_cache VALUES(?,?)',(key(docs,config,prompt),db.dumps(items)))
