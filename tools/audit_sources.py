"""Teste real e limitado de todos os canais; sem OpenAI."""
import asyncio
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import db
from app.collection import collect
from app.models import QueryInput

async def main():
    db.init()
    original_settings=db.setting()
    settings=original_settings.model_copy(deep=True)
    settings.articles_per_source=1
    db.save_settings(settings)
    query=QueryInput(countries=['BR','US','CN','RU'],start='2000-01-01',end='2099-12-31',mode='collect')
    try:
        results=await collect(query,'audit',lambda n,total,name:print(f'{n}/{total} {name}',flush=True))
    finally:
        db.save_settings(original_settings)
    report={'checked_at':db.now(),'method':'Uma leitura de artigo por canal, além do RSS/página; respeita robots.txt. Não certifica disponibilidade futura.','sources':results}
    target=Path(__file__).resolve().parents[1]/'docs'/'source-audit.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({status:sum(r['status']==status for r in results) for status in {r['status'] for r in results}},ensure_ascii=False))

if __name__=='__main__':
    asyncio.run(main())
