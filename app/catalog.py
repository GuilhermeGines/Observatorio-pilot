"""Catálogo curado. Uma URL candidata não implica integração validada."""
from urllib.parse import urlsplit

COUNTRIES = {'BR': 'Brasil', 'US': 'Estados Unidos', 'CN': 'China', 'RU': 'Rússia'}
TOPICS = {
 'geopolitica': 'Geopolítica e relações internacionais', 'politica': 'Política nacional',
 'ciencia': 'Ciência', 'fisica': 'Física', 'astronomia': 'Astronomia',
 'tecnologia': 'Tecnologia e inteligência artificial', 'economia': 'Economia e comércio',
 'clima': 'Energia, clima e meio ambiente', 'defesa': 'Defesa e segurança',
 'saude': 'Saúde e pesquisa médica'}

# id, country, name, kind, home, channel, connection, language, timezone.
# Pages use explicit bounded link discovery, feeds use RSS/Atom. Both report failures.
ROWS = [
 ('agbr','BR','Agência Brasil','jornalismo','https://agenciabrasil.ebc.com.br/','https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml','Empresa pública EBC; cobertura nacional e serviço público.','pt','America/Sao_Paulo'),
 ('g1','BR','g1','jornalismo','https://g1.globo.com/','https://g1.globo.com/rss/g1/','Grupo Globo; portal comercial de cobertura ampla.','pt','America/Sao_Paulo'),
 ('folha','BR','Folha de S.Paulo','jornalismo','https://www.folha.uol.com.br/','https://feeds.folha.uol.com.br/emcimadahora/rss091.xml','Grupo Folha; jornal comercial. Pode exigir assinatura.','pt','America/Sao_Paulo'),
 ('estadao','BR','Estadão','jornalismo','https://www.estadao.com.br/','https://www.estadao.com.br/','Grupo Estado; jornal comercial. Pode exigir assinatura.','pt','America/Sao_Paulo'),
 ('uol','BR','UOL Notícias','jornalismo','https://noticias.uol.com.br/','https://rss.uol.com.br/feed/noticias.xml','Grupo UOL/Folha; origem de propriedade relacionada à Folha, não pressupõe independência.','pt','America/Sao_Paulo'),
 ('poder360','BR','Poder360','jornalismo','https://www.poder360.com.br/','https://www.poder360.com.br/feed/','Veículo digital privado; política e poder.','pt','America/Sao_Paulo'),
 ('cnnbr','BR','CNN Brasil','jornalismo','https://www.cnnbrasil.com.br/','https://www.cnnbrasil.com.br/feed/','Operação brasileira privada licenciada da marca CNN.','pt','America/Sao_Paulo'),
 ('nexo','BR','Nexo Jornal','jornalismo','https://www.nexojornal.com.br/','https://www.nexojornal.com.br/','Jornal digital explicativo; acesso aberto e por assinatura.','pt','America/Sao_Paulo'),
 ('publica','BR','Agência Pública','jornalismo','https://apublica.org/','https://apublica.org/feed/','Organização sem fins lucrativos; investigação e interesse público.','pt','America/Sao_Paulo'),
 ('bdf','BR','Brasil de Fato','jornalismo','https://www.brasildefato.com.br/','https://www.brasildefato.com.br/feed/','Perspectiva ligada a movimentos populares; explicita posição editorial.','pt','America/Sao_Paulo'),
 ('ap','US','Associated Press','jornalismo','https://apnews.com/','https://apnews.com/','Cooperativa de notícias; agência frequentemente reproduzida por outros veículos.','en','America/New_York'),
 ('npr','US','NPR','jornalismo','https://www.npr.org/','https://feeds.npr.org/1001/rss.xml','Rede de mídia sem fins lucrativos e emissoras associadas.','en','America/New_York'),
 ('nyt','US','The New York Times','jornalismo','https://www.nytimes.com/','https://rss.nytimes.com/services/xml/rss/nyt/World.xml','The New York Times Company; jornal comercial, assinatura.','en','America/New_York'),
 ('wapo','US','The Washington Post','jornalismo','https://www.washingtonpost.com/','https://feeds.washingtonpost.com/rss/world','Jornal comercial de propriedade privada; assinatura.','en','America/New_York'),
 ('wsj','US','The Wall Street Journal','jornalismo','https://www.wsj.com/','https://feeds.content.dowjones.io/public/rss/RSSWorldNews','Dow Jones / News Corp; economia e política, assinatura.','en','America/New_York'),
 ('cnn','US','CNN','jornalismo','https://www.cnn.com/','https://www.cnn.com/','Rede comercial de notícias; CNN Brasil é uma operação licenciada distinta.','en','America/New_York'),
 ('fox','US','Fox News','jornalismo','https://www.foxnews.com/','https://moxie.foxnews.com/google-publisher/world.xml','Fox Corporation; rede comercial, com programação de notícias e opinião.','en','America/New_York'),
 ('propublica','US','ProPublica','jornalismo','https://www.propublica.org/','https://www.propublica.org/feeds/propublica/main','Organização sem fins lucrativos; jornalismo investigativo.','en','America/New_York'),
 ('ars','US','Ars Technica','jornalismo','https://arstechnica.com/','https://feeds.arstechnica.com/arstechnica/index','Condé Nast; ciência, tecnologia e políticas digitais.','en','America/New_York'),
 ('verge','US','The Verge','jornalismo','https://www.theverge.com/','https://www.theverge.com/rss/index.xml','Vox Media; tecnologia, ciência e efeitos sociais.','en','America/New_York'),
 ('xinhua','CN','Xinhua','jornalismo','https://english.news.cn/','https://english.news.cn/','Agência estatal chinesa; declarações e enquadramento institucional.','en','Asia/Shanghai'),
 ('people','CN',"People’s Daily",'jornalismo','http://en.people.cn/','http://en.people.cn/rss/World.xml','Órgão do Partido Comunista da China.','en','Asia/Shanghai'),
 ('chinadaily','CN','China Daily','jornalismo','https://www.chinadaily.com.cn/','https://www.chinadaily.com.cn/','Jornal estatal chinês voltado também ao público internacional.','en','Asia/Shanghai'),
 ('cgtn','CN','CGTN','jornalismo','https://www.cgtn.com/','https://www.cgtn.com/','Rede internacional estatal, China Media Group.','en','Asia/Shanghai'),
 ('globaltimes','CN','Global Times','jornalismo','https://www.globaltimes.cn/','https://www.globaltimes.cn/','Ligado ao People’s Daily; notícias e opinião explicitamente identificadas quando disponíveis.','en','Asia/Shanghai'),
 ('chinanews','CN','China News Service / ECNS','jornalismo','https://www.ecns.cn/','https://www.ecns.cn/','Agência estatal China News Service, edição em inglês.','en','Asia/Shanghai'),
 ('caixin','CN','Caixin Global','jornalismo','https://www.caixinglobal.com/','https://www.caixinglobal.com/','Grupo de mídia econômico; notícias e investigações, assinatura.','en','Asia/Shanghai'),
 ('sixthtone','CN','Sixth Tone','jornalismo','https://www.sixthtone.com/','https://www.sixthtone.com/','Shanghai United Media Group; instituição vinculada ao sistema estatal de mídia.','en','Asia/Shanghai'),
 ('yicai','CN','Yicai Global','jornalismo','https://www.yicaiglobal.com/','https://www.yicaiglobal.com/','Yicai / Shanghai Media Group; negócios, vínculo com mídia estatal.','en','Asia/Shanghai'),
 ('scmp','CN','South China Morning Post','jornalismo','https://www.scmp.com/','https://www.scmp.com/rss/91/feed','Sediado em Hong Kong; propriedade Alibaba. Contexto editorial distinto da China continental.','en','Asia/Hong_Kong'),
 ('tass','RU','TASS','jornalismo','https://tass.com/','https://tass.com/rss/v2.xml','Agência estatal russa; verificar reprodução da mesma origem.','en','Europe/Moscow'),
 ('ria','RU','RIA Novosti','jornalismo','https://ria.ru/','https://ria.ru/export/rss2/archive/index.xml','Agência do grupo estatal Rossiya Segodnya.','ru','Europe/Moscow'),
 ('interfax','RU','Interfax','jornalismo','https://www.interfax.ru/','https://www.interfax.ru/rss.asp','Agência de notícias comercial russa.','ru','Europe/Moscow'),
 ('rbc','RU','RBC','jornalismo','https://www.rbc.ru/','https://rssexport.rbc.ru/rbcnews/news/30/full.rss','Grupo privado de mídia econômica; algumas matérias por assinatura.','ru','Europe/Moscow'),
 ('kommersant','RU','Kommersant','jornalismo','https://www.kommersant.ru/','https://www.kommersant.ru/RSS/news.xml','Jornal comercial russo; negócios e política.','ru','Europe/Moscow'),
 ('vedomosti','RU','Vedomosti','jornalismo','https://www.vedomosti.ru/','https://www.vedomosti.ru/rss/news.xml','Jornal comercial russo; negócios, assinatura.','ru','Europe/Moscow'),
 ('rg','RU','Rossiyskaya Gazeta','jornalismo','https://rg.ru/','https://rg.ru/xml/index.xml','Jornal do governo russo, também publica atos oficiais.','ru','Europe/Moscow'),
 ('rt','RU','RT','jornalismo','https://www.rt.com/','https://www.rt.com/rss/','Rede financiada pelo Estado russo; disponibilidade varia conforme restrições locais.','en','Europe/Moscow'),
 ('moscowtimes','RU','The Moscow Times','jornalismo','https://www.themoscowtimes.com/','https://www.themoscowtimes.com/rss/news','Veículo de origem russa, independente e operando no exterior; país de origem não significa sede atual.','en','Europe/Moscow'),
 ('meduza','RU','Meduza','jornalismo','https://meduza.io/','https://meduza.io/rss2/en/all','Veículo de origem russa sediado na Letônia, independente e no exílio.','en','Europe/Moscow'),
 ('itamaraty','BR','Itamaraty','instituicao','https://www.gov.br/mre/','https://www.gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa','Ministério das Relações Exteriores; declaração oficial, não validação independente.','pt','America/Sao_Paulo'),
 ('ibge','BR','IBGE','instituicao','https://www.ibge.gov.br/','https://agenciadenoticias.ibge.gov.br/agencia-noticias.html','Instituto público de estatística; observar metodologia e revisões.','pt','America/Sao_Paulo'),
 ('inpe','BR','INPE','instituicao','https://www.gov.br/inpe/','https://www.gov.br/inpe/pt-br/assuntos/ultimas-noticias','Instituto público de pesquisas espaciais.','pt','America/Sao_Paulo'),
 ('usp','BR','Universidade de São Paulo','universidade','https://www.usp.br/','https://jornal.usp.br/feed/','Universidade pública estadual; comunicação institucional, buscar estudo original.','pt','America/Sao_Paulo'),
 ('unicamp','BR','Unicamp','universidade','https://www.unicamp.br/','https://www.unicamp.br/','Universidade pública estadual; ciência multidisciplinar.','pt','America/Sao_Paulo'),
 ('state','US','Departamento de Estado','instituicao','https://www.state.gov/','https://www.state.gov/press-releases/','Governo dos EUA; posicionamento de política externa.','en','America/New_York'),
 ('bls','US','Bureau of Labor Statistics','instituicao','https://www.bls.gov/','https://www.bls.gov/feed/bls_latest.rss','Órgão público de estatísticas do trabalho; observar revisões.','en','America/New_York'),
 ('nasa','US','NASA','instituicao','https://www.nasa.gov/','https://www.nasa.gov/feed/','Agência pública espacial; missão, pesquisa e dados.','en','America/New_York'),
 ('mit','US','Massachusetts Institute of Technology','universidade','https://www.mit.edu/','https://news.mit.edu/rss/feed','Universidade privada sem fins lucrativos; pesquisa técnica e científica.','en','America/New_York'),
 ('harvard','US','Harvard University','universidade','https://www.harvard.edu/','https://news.harvard.edu/gazette/feed/','Universidade privada sem fins lucrativos; pesquisa multidisciplinar.','en','America/New_York'),
 ('fmprc','CN','Ministério das Relações Exteriores da China','instituicao','https://www.fmprc.gov.cn/eng/','https://www.fmprc.gov.cn/eng/xw/fyrbt/','Governo chinês; entrevistas coletivas e declarações oficiais.','en','Asia/Shanghai'),
 ('statscn','CN','National Bureau of Statistics of China','instituicao','https://www.stats.gov.cn/english/','https://www.stats.gov.cn/english/PressRelease/','Órgão estatal de estatística; observar definições e séries.','en','Asia/Shanghai'),
 ('cas','CN','Chinese Academy of Sciences','instituicao','https://english.cas.cn/','https://english.cas.cn/newsroom/research_news/','Academia estatal de ciências; pesquisa e comunicados.','en','Asia/Shanghai'),
 ('tsinghua','CN','Tsinghua University','universidade','https://www.tsinghua.edu.cn/en/','https://www.tsinghua.edu.cn/en/News/LATEST_NEWS.htm','Universidade pública; pesquisa em engenharia e ciências.','en','Asia/Shanghai'),
 ('peking','CN','Peking University','universidade','https://english.pku.edu.cn/','https://newsen.pku.edu.cn/newscenter.html','Universidade pública; pesquisa multidisciplinar.','en','Asia/Shanghai'),
 ('mid','RU','Ministério das Relações Exteriores da Rússia','instituicao','https://mid.ru/en/','https://mid.ru/en/foreign_policy/news/','Governo russo; declarações oficiais e política externa.','en','Europe/Moscow'),
 ('cbr','RU','Banco da Rússia','instituicao','https://www.cbr.ru/eng/','https://www.cbr.ru/rss/RssPress','Banco central; comunicados. Séries em cbr.ru/eng/statistics.','ru','Europe/Moscow'),
 ('ras','RU','Academia Russa de Ciências','instituicao','https://www.ras.ru/','https://www.ras.ru/news.aspx','Academia pública; ciência e comunicação institucional.','ru','Europe/Moscow'),
 ('msu','RU','Universidade Estatal de Moscou','universidade','https://www.msu.ru/','https://www.msu.ru/news/','Universidade pública; pesquisa multidisciplinar.','ru','Europe/Moscow'),
 ('itmo','RU','ITMO University','universidade','https://en.itmo.ru/','https://news.itmo.ru/en/','Universidade pública; fotônica, computação e tecnologia.','en','Europe/Moscow'),
]

SOURCES = [dict(zip(('id','country','name','kind','home','channel','affiliation','language','timezone'), row)) for row in ROWS]
for source in SOURCES:
    source['connector'] = 'page' if source['channel'].endswith(('/', '.htm', '.html')) and not any(x in source['channel'] for x in ('feed/', 'rss/')) else 'feed'
    if source['id'] in {'chinadaily','nexo','estadao','ap','cnn','xinhua','cgtn','globaltimes','chinanews','caixin','sixthtone','yicai','itamaraty','ibge','inpe','unicamp','state','fmprc','statscn','cas','tsinghua','peking','mid','ras','msu','itmo'}:
        source['connector'] = 'page'
    source['domains'] = list({urlsplit(source['home']).hostname, urlsplit(source['channel']).hostname})
    source['reference'] = source['home']
    source['coverage_note'] = 'Canal recente, sem garantia de arquivo histórico completo. Vínculo institucional não determina veracidade.'
from .catalog_expansion import expand
expand(SOURCES)
BY_ID = {s['id']: s for s in SOURCES}

def source_route(query):
    from .source_routing import route
    return getattr(query,'_source_route',None) or route(query,SOURCES)

def selected_sources(query):
    ids=set(source_route(query)['source_ids'])
    return [s for s in SOURCES if s['id'] in ids]
