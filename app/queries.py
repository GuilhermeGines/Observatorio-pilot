import json
import re
from datetime import datetime
from difflib import SequenceMatcher
from itertools import combinations
from . import db
from .catalog import BY_ID, COUNTRIES, source_route
from .collection import folded, publication

def matching(rows, query, disabled=()):
    result=[]
    source_ids=set(source_route(query)['source_ids'])
    for row in rows:
        if row['source_id'] not in source_ids or row['source_id'] in disabled:
            continue
        published=publication(row.get('published_at'),BY_ID[row['source_id']]['timezone'])[0]
        if not published or not str(query.start)<=published[:10]<=str(query.end):
            continue
        if query.keyword and folded(query.keyword) not in folded(row['title']+' '+row['text']):
            continue
        if query.topics and not set(query.topics).intersection(row.get('topics',[])):
            continue
        result.append(row|{'published_at':published})
    return sorted(result,key=lambda row:row['published_at'],reverse=True)

STOP=set('the and for with from that this have has said says are was were after over under new not but para pela pelo uma como que dos das com por sobre mais its into amid first will news than their they his her world china russia brazil united states brasil estados unidos rússia russian chinese news'.split())
def title_terms(row):
    return {t for t in re.findall(r'[^\W\d_]+',folded(row['title'])) if len(t)>=4 and t not in STOP}

def related_pairs(documents):
    pairs=[]
    # Candidate blocking by shared topic first; no model-wide all-to-all comparison.
    buckets={}
    for doc in documents:
        for topic in doc['topics']:
            buckets.setdefault(topic,[]).append(doc)
    seen=set()
    for topic,docs in buckets.items():
        for a,b in combinations(docs,2):
            ids=tuple(sorted([a['revision_id'],b['revision_id']]))
            if ids in seen:
                continue
            common=title_terms(a)&title_terms(b)
            days=abs((datetime.fromisoformat(a['published_at']).date()-datetime.fromisoformat(b['published_at']).date()).days)
            if (len(common)>=2 and days<=45) or len(common)>=3:
                seen.add(ids)
                pairs.append({'revision_ids':list(ids),'shared_terms':sorted(common),'topic':topic,'days_apart':days,'relation':'candidatos_temporais' if days<=45 else 'candidatos_historicos'})
    return pairs[:100]

def origin_groups(documents):
    parents={d['revision_id']:d['revision_id'] for d in documents}
    def root(x):
        while parents[x]!=x:
            x=parents[x]
        return x
    reasons={}
    for a,b in combinations(documents,2):
        same_credit=bool(a.get('origin')) and a.get('origin')==b.get('origin')
        similar=SequenceMatcher(None,folded(a['title']),folded(b['title'])).ratio()>.88
        same_text=len(a['text'])>100 and a['text']==b['text']
        if same_text or similar or (same_credit and bool(title_terms(a)&title_terms(b))):
            parents[root(b['revision_id'])]=root(a['revision_id'])
            reasons[(a['revision_id'],b['revision_id'])]='Texto/título semelhante ou crédito de origem comum; independência não estabelecida.'
    groups={}
    for doc in documents:
        groups.setdefault(root(doc['revision_id']),[]).append(doc['revision_id'])
    return [{'revision_ids':ids,'note':'Agrupamento preventivo por crédito ou semelhança. Não representa confirmações independentes.'} for ids in groups.values() if len(ids)>1]

def make_result(query,coverage=None):
    settings=db.setting()
    routing=source_route(query)
    routed_ids=set(routing['source_ids'])
    routing['disabled_count']=len(routed_ids.intersection(settings.disabled_sources))
    rows=db.revision_rows()
    matched=matching(rows,query,settings.disabled_sources)
    # Keep high-volume feeds from crowding an entire country's perspective out.
    queues={sid:[r for r in matched if r['source_id']==sid] for sid in BY_ID}
    selected=[]
    while any(queues.values()) and len(selected)<200:
        for items in queues.values():
            if items and len(selected)<200:
                selected.append(items.pop(0))
    documents=[]
    for row in selected:
        source=BY_ID[row['source_id']]
        documents.append({k:v for k,v in row.items() if k!='body'} | {'source_name':source['name'],'affiliation':source['affiliation'],'source_kind':source['kind']})
    source_state={s['id']:s for s in db.sources()}
    if coverage is None:
        coverage=[{'source_id':s['id'],'status':'desativada' if s['id'] in settings.disabled_sources else 'acervo',
            'checked_at':s['checked_at'],'last_status':s['status'],'detail':{'message':'Consulta somente ao acervo local; nenhuma coleta nova foi feita.'}} for s in source_state.values() if s['id'] in routed_ids]
    for item in coverage:
        item['name']=BY_ID[item['source_id']]['name']
        item['country']=BY_ID[item['source_id']]['country']
        item['matches']=sum(d['source_id']==item['source_id'] for d in matched)
        item['displayed_matches']=sum(d['source_id']==item['source_id'] for d in documents)
    undated=sum(not r.get('published_at') and r['source_id'] in routed_ids and r['source_id'] not in settings.disabled_sources for r in rows)
    return {'routing':routing,'filters':query.model_dump(mode='json'),'documents':documents,'total_matches':len(matched),'truncated':len(matched)>200,
        'coverage':coverage,'undated_excluded':undated,'origin_groups':origin_groups(documents),'related_pairs':related_pairs(documents),
        'country_summaries':[{'country':c,'name':COUNTRIES[c],'count':sum(d['country']==c for d in documents),
            'text':f"{sum(d['country']==c for d in documents)} documentos no recorte consultado. Resumo interpretativo em português disponível mediante análise com IA."} for c in query.countries],
        'limitations':['Consulta por data de publicação declarada, no fuso editorial da fonte; data de coleta registrada separadamente.',
          'Busca literal sem distinção de acentos/maiúsculas, nos títulos e textos efetivamente lidos. Não traduz automaticamente palavras-chave.',
          'Temas são etiquetas automáticas por vocabulário multilíngue; podem haver omissões e falsos positivos.',
          'Até 200 documentos são exibidos, alternando as fontes com resultados para preservar diversidade. A contagem de cobertura inclui todas as correspondências no acervo; documentos fora do limite não são enviados à análise.',
          'Canais recentes e leituras limitadas não garantem recuperar arquivos antigos. Ausência no acervo não significa inexistência da notícia.',
          'Fontes sem conteúdo ou data verificável são excluídas da análise. Uma declaração oficial é evidência do posicionamento da instituição.',
          'Semelhança textual não estabelece correlação estatística, causalidade nem confirmação independente.'],
        'created_at':db.now()}

def read_query(query_id):
    with db.connect() as connection:
        row=connection.execute('SELECT * FROM queries WHERE id=?',(query_id,)).fetchone()
        if not row:
            return None
        analyses=[dict(r) for r in connection.execute('SELECT * FROM analyses WHERE query_id=? ORDER BY version DESC',(query_id,))]
        for analysis in analyses:
            for field in ['config','result','usage']:
                analysis[field]=json.loads(analysis[field])
            analysis['audio']=[dict(a) for a in connection.execute('SELECT * FROM audio WHERE analysis_id=?',(analysis['id'],))]
    return dict(row)|{'filters':json.loads(row['filters']),'result':json.loads(row['result']) if row['result'] else None,'analyses':analyses}
