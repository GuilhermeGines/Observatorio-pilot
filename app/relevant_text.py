import re
from difflib import SequenceMatcher
from .collection import folded, KEYWORDS
from .models import SummaryOutput

def select(document,keyword,topics,limit):
    text=document['text']
    paragraphs=[p.strip() for p in re.split(r'\n\s*\n|\n',text) if p.strip()]
    # Long unstructured paragraphs become literal sentence/chunk spans.
    spans=[]
    for paragraph in paragraphs:
        for sentence in re.split(r'(?<=[.!?。！？])\s+',paragraph):
            spans.extend(sentence[i:i+400] for i in range(0,len(sentence),400))
    terms=[t for t in re.findall(r'\w+',folded(keyword)) if len(t)>2]
    terms+= [folded(t) for topic in topics for t in KEYWORDS.get(topic,[])]
    scores=[sum(folded(span).count(t) for t in terms) for span in spans]
    order=sorted(range(len(spans)),key=lambda i:(-scores[i],i))
    chosen=set();used=0
    for i in order:
        if any(scores) and scores[i]==0: continue
        # Prioritize matching span, then its adjacent context within the same budget.
        for j in [i,i-1,i+1]:
            if 0<=j<len(spans) and j not in chosen and used+len(spans[j])+(2 if chosen else 0)<=limit:
                used+=len(spans[j])+(2 if chosen else 0);chosen.add(j)
    selected=[{'id':f"r{document['revision_id']}p{i}",'text':spans[i]} for i in sorted(chosen)]
    return {'revision_id':document['revision_id'],'country':document['country'],'source_name':document['source_name'],
            'title':document['title'],'paragraphs':selected,'text':'\n\n'.join(p['text'] for p in selected)}

def group_duplicates(documents):
    representatives=[];groups=[]
    for doc in documents:
        match=next((d for d in representatives if d['country']==doc['country'] and
            (folded(d['text'])==folded(doc['text']) or
             (min(len(d['text']),len(doc['text']))>400 and
              SequenceMatcher(None,folded(d['title']),folded(doc['title'])).ratio()>.85 and
              SequenceMatcher(None,folded(d['text'][:6000]),folded(doc['text'][:6000])).ratio()>.94))),None)
        if match:
            groups.append({'representative':match['revision_id'],'revision_id':doc['revision_id'],'source_name':doc['source_name'],'url':doc.get('url','')})
        else: representatives.append(doc)
    return representatives,groups

def resolve(stage,payload):
    paragraphs={p['id']:(d,p['text']) for d in payload['documents'] for p in d.get('paragraphs',[])}
    points=[];counts={}
    for point in stage.summaries:
        counts[point.country]=counts.get(point.country,0)+1
        if counts[point.country]>5: raise ValueError('A síntese excedeu cinco pontos por país.')
        evidence=[]
        for identifier in dict.fromkeys(point.paragraph_ids):
            if identifier not in paragraphs: raise ValueError('Referência a parágrafo não enviado; síntese rejeitada.')
            doc,quote=paragraphs[identifier]
            if doc['country']!=point.country: raise ValueError('País incompatível com o parágrafo citado.')
            evidence.append({'revision_id':doc['revision_id'],'quote':quote})
        points.append({'country':point.country,'text':point.text,'evidence':evidence})
    return SummaryOutput(summaries=points,gaps=stage.gaps)
