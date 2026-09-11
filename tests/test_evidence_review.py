import pytest
from app.ai import validate_evidence
from app.evidence_review import literal_quote,review
from test_core import synthetic_analysis

def test_formatting_restores_exact_original_without_accepting_paraphrase():
    assert literal_quote('A “amostra” tem dez unidades.','A "amostra" tem\n dez unidades.')=='A "amostra" tem\n dez unidades.'
    assert literal_quote('A amostra tem onze unidades.','A amostra tem dez unidades.') is None

def test_preserves_verified_items_and_rejects_invalid_script():
    text='A amostra contém dez unidades.'
    result=synthetic_analysis(1,text)
    result.summaries.append(result.summaries[0].model_copy(deep=True))
    result.summaries[-1].evidence[0].quote='A amostra contém cem unidades.'
    result.script='A amostra contém cem unidades.'
    payload={'documents':[{'revision_id':1,'text':text,'country':'BR'}],'allowed_comparison_pairs':[]}
    clean,report=review(result,payload,validate_evidence)
    assert report['discarded']==1
    assert 'cem unidades' not in clean.script
    validate_evidence(clean,payload)
    for field in ['summaries','claims','comparisons','cross_statements']:
        for item in getattr(result,field):
            for evidence in item.evidence:
                evidence.revision_id=999
    with pytest.raises(ValueError,match='nenhum resumo'):
        review(result,payload,validate_evidence)
