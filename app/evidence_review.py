"""Ajusta somente espaços/aspas e descarta itens sem referências verificáveis."""
from .models import AnalysisOutput

FIELDS=('summaries','claims','comparisons','cross_statements')

def literal_quote(quote, text):
    if quote.strip() and quote in text:
        return quote
    def normalize(value):
        chars=[]; positions=[]
        for index,char in enumerate(value):
            char={'“':'"','”':'"','‘':"'",'’':"'"}.get(char,char)
            char=' ' if char.isspace() else char
            if char==' ' and chars and chars[-1]==' ':
                continue
            chars.append(char);positions.append(index)
        return ''.join(chars),positions
    needle,_=normalize(quote.strip())
    haystack,positions=normalize(text)
    if not needle:
        return None
    start=haystack.find(needle)
    return text[positions[start]:positions[start+len(needle)-1]+1] if start>=0 else None

def review(result,payload,validate):
    docs={d['revision_id']:d for d in payload['documents']}
    checked=result.model_copy(deep=True)
    report={'discarded':0,'format_adjustments':0,'retained':0}
    for field in FIELDS:
        accepted=[]
        for item in getattr(checked,field):
            for evidence in item.evidence:
                doc=docs.get(evidence.revision_id)
                if doc:
                    exact=literal_quote(evidence.quote,doc['text'])
                    if exact is not None and exact!=evidence.quote:
                        evidence.quote=exact
                        report['format_adjustments']+=1
            probe=AnalysisOutput(**{k:[item] if k==field else [] for k in FIELDS},gaps=[],script='')
            try:
                validate(probe,payload)
            except ValueError:
                report['discarded']+=1
            else:
                accepted.append(item)
                report['retained']+=1
        setattr(checked,field,accepted)
    if not report['retained'] and report['discarded']:
        raise ValueError('O Qwen terminou, mas nenhum resumo ou afirmação passou na verificação de referências. Não há análise validada para salvar. Os documentos originais permanecem disponíveis.')
    if report['discarded']:
        checked.gaps.insert(0,f"Análise parcial: {report['discarded']} itens foram descartados por referência, trecho ou atribuição inválidos. A presença de uma citação não garante que a interpretação esteja correta.")
        # Do not retain a script based on rejected material.
        checked.script=' '.join(s.text for s in checked.summaries)
    return checked,report
