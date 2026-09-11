"""Read-only channel check: no article reads, DB writes or model calls."""
import asyncio
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.catalog import SOURCES
from app.collection import Reader, feed_entries, page_entries, safe_error

async def main():
    semaphore=asyncio.Semaphore(8)
    results=[]
    async def one(source):
        async with semaphore:
            reader=Reader()
            row={'id':source['id'],'channel':source['channel']}
            try:
                async with asyncio.timeout(22):
                    content,ctype,url=await reader.get(source['channel'],source)
                    entries=feed_entries(content,source) if source['connector']=='feed' else page_entries(content.decode('utf-8',errors='replace'),source)
                    row.update(status='candidatos' if entries else 'sem_itens',candidates=len(entries),dated=sum(bool(b.get('published_at')) for _,b in entries),final_url=url)
            except Exception as error:
                row.update(status='indisponivel',reason=safe_error(error))
            finally:
                await reader.close()
            results.append(row)
    await asyncio.gather(*(one(s) for s in SOURCES))
    out=Path(__file__).resolve().parents[1]/'docs/catalog-channels.json'
    out.write_text(json.dumps({'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'Somente canais e metadados; sem artigos ou análise. Candidatos não confirmam extração de texto.','sources':results},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(Counter(r['status'] for r in results))))
if __name__=='__main__': asyncio.run(main())
