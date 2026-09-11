"""Curadoria por cobertura editorial/científica, não ranking absoluto.

Uma fonte pode ocupar vários grupos, mas é coletada uma única vez.
Os canais são candidatos públicos; disponibilidade é informada pela coleta.
"""

# id | país | nome | tipo | canal | conector
ADDITIONS = '''
planalto|BR|Presidência da República — Planalto|instituicao|https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/noticias|page
ufrj|BR|Universidade Federal do Rio de Janeiro|universidade|https://conexao.ufrj.br/feed/|feed
ufmg|BR|Universidade Federal de Minas Gerais|universidade|https://ufmg.br/comunicacao/noticias|page
unesp|BR|Universidade Estadual Paulista|universidade|https://jornal.unesp.br/feed/|feed
tecnoblog|BR|Tecnoblog|jornalismo|https://tecnoblog.net/feed/|feed
canaltech|BR|Canaltech|jornalismo|https://canaltech.com.br/rss/|feed
tecmundo|BR|TecMundo|jornalismo|https://rss.tecmundo.com.br/feed|feed
macmagazine|BR|MacMagazine|jornalismo|https://macmagazine.com.br/feed/|feed
olhardigital|BR|Olhar Digital|jornalismo|https://olhardigital.com.br/feed/|feed
fapesp|BR|Agência FAPESP|instituicao|https://agencia.fapesp.br/|page
pesquisafapesp|BR|Pesquisa FAPESP|jornalismo|https://revistapesquisa.fapesp.br/feed/|feed
sbpc|BR|Sociedade Brasileira para o Progresso da Ciência|instituicao|https://portal.sbpcnet.org.br/feed/|feed
cbpf|BR|Centro Brasileiro de Pesquisas Físicas|instituicao|https://www.gov.br/cbpf/pt-br/assuntos/noticias|page
cnpem|BR|Centro Nacional de Pesquisa em Energia e Materiais|instituicao|https://cnpem.br/feed/|feed
on|BR|Observatório Nacional|instituicao|https://www.gov.br/observatorio/pt-br/assuntos/noticias|page
aeb|BR|Agência Espacial Brasileira|instituicao|https://www.gov.br/aeb/pt-br/assuntos/noticias|page
valor|BR|Valor Econômico|jornalismo|https://valor.globo.com/|page
infomoney|BR|InfoMoney|jornalismo|https://www.infomoney.com.br/feed/|feed
oeco|BR|O Eco|jornalismo|https://oeco.org.br/feed/|feed
climainfo|BR|ClimaInfo|jornalismo|https://climainfo.org.br/feed/|feed
epbr|BR|agência epbr|jornalismo|https://epbr.com.br/feed/|feed
defesanet|BR|DefesaNet|jornalismo|https://www.defesanet.com.br/feed/|feed
defesaaerea|BR|Defesa Aérea & Naval|jornalismo|https://www.defesaaereanaval.com.br/feed|feed
naval|BR|Poder Naval|jornalismo|https://www.naval.com.br/blog/feed/|feed
defesabr|BR|Ministério da Defesa do Brasil|instituicao|https://www.gov.br/defesa/pt-br/centrais-de-conteudo/noticias|page
fiocruz|BR|Fundação Oswaldo Cruz|instituicao|https://agencia.fiocruz.br/noticias|page
butantan|BR|Instituto Butantan|instituicao|https://butantan.gov.br/noticias|page
saudebr|BR|Ministério da Saúde do Brasil|instituicao|https://www.gov.br/saude/pt-br/assuntos/noticias|page
whitehouse|US|Casa Branca|instituicao|https://www.whitehouse.gov/news/|page
stanford|US|Stanford University|universidade|https://news.stanford.edu/|page
princeton|US|Princeton University|universidade|https://www.princeton.edu/news|page
caltech|US|California Institute of Technology|universidade|https://www.caltech.edu/about/news|page
foreignaffairs|US|Foreign Affairs|jornalismo|https://www.foreignaffairs.com/|page
foreignpolicy|US|Foreign Policy|jornalismo|https://foreignpolicy.com/feed/|feed
politico|US|Politico|jornalismo|https://www.politico.com/rss/politicopicks.xml|feed
sciencenews|US|Science News|jornalismo|https://www.sciencenews.org/feed|feed
science|US|Science — AAAS|jornalismo|https://www.science.org/news|page
scientificamerican|US|Scientific American|jornalismo|https://www.scientificamerican.com/|page
aps|US|Physics — American Physical Society|instituicao|https://physics.aps.org/|page
physicstoday|US|Physics Today — AIP|jornalismo|https://pubs.aip.org/physicstoday|page
slac|US|SLAC National Accelerator Laboratory|instituicao|https://www6.slac.stanford.edu/news|page
fermilab|US|Fermilab|instituicao|https://news.fnal.gov/feed/|feed
space|US|Space.com|jornalismo|https://www.space.com/feeds/all|feed
astronomy|US|Astronomy Magazine|jornalismo|https://www.astronomy.com/feed/|feed
skyandtelescope|US|Sky & Telescope|jornalismo|https://skyandtelescope.org/feed/|feed
wired|US|WIRED|jornalismo|https://www.wired.com/feed/rss|feed
techcrunch|US|TechCrunch|jornalismo|https://techcrunch.com/feed/|feed
engadget|US|Engadget|jornalismo|https://www.engadget.com/rss.xml|feed
bloomberg|US|Bloomberg|jornalismo|https://feeds.bloomberg.com/markets/news.rss|feed
cnbc|US|CNBC|jornalismo|https://www.cnbc.com/id/100003114/device/rss/rss.html|feed
fed|US|Federal Reserve|instituicao|https://www.federalreserve.gov/feeds/press_all.xml|feed
noaa|US|NOAA|instituicao|https://www.noaa.gov/news|page
insideclimate|US|Inside Climate News|jornalismo|https://insideclimatenews.org/feed/|feed
grist|US|Grist|jornalismo|https://grist.org/feed/|feed
eia|US|Energy Information Administration|instituicao|https://www.eia.gov/todayinenergy/|page
defensenews|US|Defense News|jornalismo|https://www.defensenews.com/|page
breakingdefense|US|Breaking Defense|jornalismo|https://breakingdefense.com/feed/|feed
defenseone|US|Defense One|jornalismo|https://www.defenseone.com/|page
stripes|US|Stars and Stripes|jornalismo|https://www.stripes.com/|page
dod|US|Departamento de Defesa dos EUA|instituicao|https://www.defense.gov/News/|page
nih|US|National Institutes of Health|instituicao|https://www.nih.gov/news-events/news-releases|page
cdc|US|Centers for Disease Control and Prevention|instituicao|https://www.cdc.gov/media/|page
kff|US|KFF Health News|jornalismo|https://kffhealthnews.org/feed/|feed
stat|US|STAT|jornalismo|https://www.statnews.com/feed/|feed
statecouncil|CN|Conselho de Estado da China|instituicao|https://english.www.gov.cn/news/|page
zhejiang|CN|Zhejiang University|universidade|https://www.zju.edu.cn/english/|page
sjtu|CN|Shanghai Jiao Tong University|universidade|https://en.sjtu.edu.cn/news|page
fudan|CN|Fudan University|universidade|https://www.fudan.edu.cn/en/|page
sciencenet|CN|ScienceNet China|jornalismo|https://news.sciencenet.cn/|page
stdaily|CN|Science and Technology Daily|jornalismo|https://www.stdaily.com/|page
ihep|CN|Institute of High Energy Physics — CAS|instituicao|https://english.ihep.cas.cn/nw/|page
iopcas|CN|Institute of Physics — CAS|instituicao|https://english.iop.cas.cn/|page
nao|CN|National Astronomical Observatories — CAS|instituicao|https://english.nao.cas.cn/|page
cnsa|CN|China National Space Administration|instituicao|https://www.cnsa.gov.cn/english/|page
pmo|CN|Purple Mountain Observatory — CAS|instituicao|https://english.pmo.cas.cn/|page
36kr|CN|36Kr|jornalismo|https://36kr.com/feed|feed
ithome|CN|IT Home|jornalismo|https://www.ithome.com/rss/|feed
geekpark|CN|GeekPark|jornalismo|https://www.geekpark.net/|page
pingwest|CN|PingWest|jornalismo|https://en.pingwest.com/|page
technode|CN|TechNode|jornalismo|https://technode.com/feed/|feed
cma|CN|China Meteorological Administration|instituicao|https://www.cma.gov.cn/en2014/|page
mee|CN|Ministério da Ecologia e Meio Ambiente da China|instituicao|https://english.mee.gov.cn/|page
nea|CN|National Energy Administration|instituicao|https://www.nea.gov.cn/|page
modcn|CN|Ministério da Defesa da China|instituicao|http://eng.mod.gov.cn/|page
81cn|CN|China Military Online|jornalismo|http://eng.chinamil.com.cn/|page
nhc|CN|National Health Commission|instituicao|http://en.nhc.gov.cn/|page
chinacdc|CN|Chinese Center for Disease Control and Prevention|instituicao|https://en.chinacdc.cn/|page
kremlin|RU|Presidência da Rússia — Kremlin|instituicao|https://en.kremlin.ru/events/president/news|page
spbu|RU|Saint Petersburg State University|universidade|https://english.spbu.ru/news-events/news|page
mipt|RU|Moscow Institute of Physics and Technology|universidade|https://mipt.ru/news/|page
hse|RU|HSE University|universidade|https://www.hse.ru/en/news/|page
nplus1|RU|N + 1|jornalismo|https://nplus1.ru/rss|feed
indicator|RU|Indicator|jornalismo|https://indicator.ru/|page
elementy|RU|Elementy|jornalismo|https://elementy.ru/rss/news|feed
jinr|RU|Joint Institute for Nuclear Research — Dubna|instituicao|https://www.jinr.ru/posts/category/news/|page
roscosmos|RU|Roscosmos|instituicao|https://www.roscosmos.ru/|page
iki|RU|Space Research Institute — RAS|instituicao|https://iki.cosmos.ru/news|page
inasan|RU|Institute of Astronomy — RAS|instituicao|https://www.inasan.ru/|page
3dnews|RU|3DNews|jornalismo|https://3dnews.ru/news/rss/|feed
ixbt|RU|iXBT|jornalismo|https://www.ixbt.com/export/news.rss|feed
cnews|RU|CNews|jornalismo|https://www.cnews.ru/inc/rss/news.xml|feed
habr|RU|Habr|jornalismo|https://habr.com/ru/rss/news/|feed
roshydromet|RU|Roshydromet|instituicao|https://www.meteorf.gov.ru/|page
meteoinfo|RU|Hydrometeorological Centre of Russia|instituicao|https://meteoinfo.ru/novosti|page
energyru|RU|Ministério da Energia da Rússia|instituicao|https://minenergo.gov.ru/|page
modru|RU|Ministério da Defesa da Rússia|instituicao|https://mil.ru/|page
redstar|RU|Krasnaya Zvezda|jornalismo|https://redstar.ru/feed/|feed
minzdrav|RU|Ministério da Saúde da Rússia|instituicao|https://minzdrav.gov.ru/news|page
rospotrebnadzor|RU|Rospotrebnadzor|instituicao|https://www.rospotrebnadzor.ru/|page
medvestnik|RU|Medvestnik|jornalismo|https://medvestnik.ru/|page
'''

GENERAL = {
 'BR':'agbr g1 folha estadao uol poder360 cnnbr nexo publica bdf',
 'US':'ap npr nyt wapo wsj cnn fox propublica ars verge',
 'CN':'xinhua people chinadaily cgtn globaltimes chinanews caixin sixthtone yicai scmp',
 'RU':'tass ria interfax rbc kommersant vedomosti rg rt moscowtimes meduza',
}
GOVERNMENT = {'BR':'planalto','US':'whitehouse','CN':'statecouncil','RU':'kremlin'}
UNIVERSITIES = {
 'BR':'usp unicamp ufrj ufmg unesp',
 'US':'mit harvard stanford princeton caltech',
 'CN':'tsinghua peking zhejiang sjtu fudan',
 'RU':'msu itmo spbu mipt hse',
}
GROUPS = {
 'BR': {
  'geopolitica':'itamaraty agbr folha poder360 cnnbr',
  'politica':'agbr g1 folha poder360 publica',
  'ciencia':'fapesp pesquisafapesp usp unicamp sbpc',
  'fisica':'cbpf cnpem pesquisafapesp usp unicamp',
  'astronomia':'inpe on aeb usp pesquisafapesp',
  'tecnologia':'tecnoblog canaltech tecmundo macmagazine olhardigital',
  'economia':'valor infomoney ibge agbr folha',
  'clima':'inpe oeco publica climainfo epbr',
  'defesa':'defesanet defesaaerea naval agbr defesabr',
  'saude':'fiocruz butantan saudebr agbr pesquisafapesp',
 },
 'US': {
  'geopolitica':'ap npr foreignaffairs foreignpolicy state',
  'politica':'ap npr nyt wapo politico',
  'ciencia':'sciencenews science scientificamerican mit harvard',
  'fisica':'aps physicstoday slac fermilab caltech',
  'astronomia':'nasa space astronomy skyandtelescope caltech',
  'tecnologia':'ars verge wired techcrunch engadget',
  'economia':'wsj bloomberg cnbc bls fed',
  'clima':'noaa insideclimate grist eia nasa',
  'defesa':'defensenews breakingdefense defenseone stripes dod',
  'saude':'nih cdc kff stat harvard',
 },
 'CN': {
  'geopolitica':'xinhua people cgtn scmp fmprc',
  'politica':'xinhua people chinadaily caixin cgtn',
  'ciencia':'cas sciencenet stdaily tsinghua peking',
  'fisica':'ihep iopcas fudan sciencenet cas',
  'astronomia':'cas nao cnsa pmo xinhua',
  'tecnologia':'36kr ithome geekpark pingwest technode',
  'economia':'caixin yicai scmp statscn chinadaily',
  'clima':'cma mee nea cas chinadaily',
  'defesa':'modcn 81cn xinhua cgtn scmp',
  'saude':'nhc chinacdc cas fudan peking',
 },
 'RU': {
  'geopolitica':'tass interfax kommersant mid meduza',
  'politica':'tass ria rbc meduza moscowtimes',
  'ciencia':'nplus1 indicator elementy ras msu',
  'fisica':'jinr mipt elementy ras msu',
  'astronomia':'roscosmos iki inasan nplus1 ras',
  'tecnologia':'3dnews ixbt cnews habr nplus1',
  'economia':'rbc vedomosti kommersant cbr interfax',
  'clima':'roshydromet meteoinfo energyru nplus1 ras',
  'defesa':'tass interfax kommersant modru redstar',
  'saude':'minzdrav rospotrebnadzor medvestnik nplus1 indicator',
 },
}

def expand(sources):
    from urllib.parse import urlsplit
    for line in ADDITIONS.strip().splitlines():
        sid,country,name,kind,channel,connector=line.split('|')
        home=f'{urlsplit(channel).scheme}://{urlsplit(channel).netloc}/'
        if urlsplit(channel).hostname=='www.gov.br':
            home='https://www.gov.br/'+urlsplit(channel).path.strip('/').split('/')[0]+'/'
        sources.append(dict(id=sid,country=country,name=name,kind=kind,home=home,channel=channel,
            connector=connector,domains=[urlsplit(channel).hostname],reference=channel,
            language={'BR':'pt','US':'en','CN':'zh','RU':'ru'}[country],
            timezone={'BR':'America/Sao_Paulo','US':'America/New_York','CN':'Asia/Shanghai','RU':'Europe/Moscow'}[country],
            affiliation=('Comunicação universitária; conferir o estudo original.' if kind=='universidade' else
                'Fonte institucional; declarações não são confirmação independente.' if kind=='instituicao' else
                'Publicação editorial temática; distinguir reportagem, opinião, publicidade e reprodução de terceiros.'),
            coverage_note='Canal público recente. Cadastro não garante acesso, data extraível ou arquivo histórico completo.'))
    for s in sources:
        country=s['country']; sid=s['id']
        s['topics']=[topic for topic,ids in GROUPS[country].items() if sid in ids.split()]
        s['groups']=(['jornalismo_geral'] if sid in GENERAL[country].split() else []) + (['governo'] if sid==GOVERNMENT[country] else []) + (['universidades'] if sid in UNIVERSITIES[country].split() else [])
        s['selection_note']='Curadoria por especialização, relevância nacional e produção científica; não constitui ranking absoluto.'
        if urlsplit(s['home']).hostname=='www.gov.br':
            s['path_prefix']=urlsplit(s['home']).path
    homes={'tecmundo':'https://www.tecmundo.com.br/','bloomberg':'https://www.bloomberg.com/','ufrj':'https://ufrj.br/','unesp':'https://www.unesp.br/','fermilab':'https://www.fnal.gov/','slac':'https://www6.slac.stanford.edu/'}
    for s in sources:
        if s['id'] in homes:
            s['home']=homes[s['id']]
            s['domains'].append(urlsplit(s['home']).hostname)
        if s['id'] in {'stanford','caltech','slac'}: s['timezone']='America/Los_Angeles'
    # Explicit language exceptions for English-language editions.
    for s in sources:
        if s['id'] in {'statecouncil','zhejiang','sjtu','fudan','ihep','iopcas','nao','cnsa','pmo','pingwest','technode','cma','mee','modcn','81cn','nhc','chinacdc','kremlin','spbu','hse'}:
            s['language']='en'
    notes={
      'habr':'Plataforma de notícias e comunidade tecnológica; textos de usuários e empresas exigem atribuição explícita.',
      '81cn':'Publicação militar oficial chinesa; evidencia a posição institucional, não confirmação independente.',
      'redstar':'Publicação militar oficial russa; evidencia a posição institucional, não confirmação independente.',
      'jinr':'Organização científica intergovernamental sediada em Dubna, Rússia; não exclusivamente nacional.',
      'pesquisafapesp':'Jornalismo científico ligado à FAPESP; conferir estudos originais.',
      'stripes':'Publicação para a comunidade militar dos EUA; distinguir vínculo institucional e independência editorial.',
    }
    for s in sources:
        if s['id'] in notes: s['affiliation']=notes[s['id']]
