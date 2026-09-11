import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import db,ai

@pytest.fixture(autouse=True)
def isolated_data(tmp_path,monkeypatch):
    monkeypatch.setattr(db,'DATA',tmp_path/'data')
    monkeypatch.setattr(ai,'get_key',lambda:'')
    db.init()
    yield

@pytest.fixture
def synthetic_document():
    from app.collection import base_body
    from app.catalog import BY_ID
    d=base_body(BY_ID['agbr'],'FIXTURE SINTÉTICA — Samsung energia pesquisa','Exemplo sintético: o Instituto Alfa afirmou que a pesquisa de energia Samsung mediu 10 unidades.','2026-09-07T23:30:00-03:00','Redação de teste')
    d.update(access='texto_extraido',genre='apuracao_nao_verificada',origin='')
    return d
