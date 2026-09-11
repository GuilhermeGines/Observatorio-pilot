# Catálogo ampliado do Observatório

170 fontes únicas. Cada país tem 5 fontes em cada um dos 10 temas, 10 veículos jornalísticos, 1 governo principal e 5 universidades. As 66 participações por país não são 66 fontes distintas: uma fonte pode integrar vários grupos, sem duplicar a coleta.

Seleção editorial por relevância nacional, especialização e produção científica, sem afirmar ranking absoluto. Preserva os veículos anteriores e acrescenta fontes especializadas. Universidades selecionadas entre instituições de destaque; há cinco nos quatro países. Instituições científicas e ministérios temáticos não são contados como o governo principal. País representa origem/contexto editorial; JINR é intergovernamental, sediado na Rússia.

## Roteamento antes da coleta

Palavras reconhecidas selecionam temas diretamente. Expressões desconhecidas passam por classificação local no Ollama, somente com a expressão e os nomes dos temas, até 128 tokens de resposta, sem documentos e sem OpenAI. O resultado é reutilizado durante a sessão. A seleção explícita de tema permite buscar sem classificação por IA. Ambiguidade, indisponibilidade ou conflito pedem seleção de tema, sem consultar fontes. Sem expressão nem tema, são usados os dez veículos gerais por país. O acervo obedece à mesma seleção de fontes. Isso reduz buscas irrelevantes, mas a classificação semântica não é infalível; o tema escolhido aparece no resultado.

Nenhuma busca real nem geração Qwen foi executada para validar o roteamento. Apenas quatro testes simulados e compilação.

## Referências da curadoria

- [QS 2026](https://www.qs.com/insights/qs-world-university-rankings-2026)
- [Universidades brasileiras — QS](https://www.topuniversities.com/world-university-rankings?countries=br&tab=indicators)
- [Universidades chinesas — ShanghaiRanking](https://www.shanghairanking.com/rankings/bcur/202611)
- [Universidades russas — QS](https://www.topuniversities.com/world-university-rankings/2026?countries=ru)

Rankings são referências auxiliares, não uma ordem universal de qualidade nem o único critério da seleção. As páginas oficiais das fontes constam abaixo.

## Brasil

43 fontes únicas.

**Veículos jornalísticos:** [Agência Brasil](https://agenciabrasil.ebc.com.br/); [g1](https://g1.globo.com/); [Folha de S.Paulo](https://www.folha.uol.com.br/); [Estadão](https://www.estadao.com.br/); [UOL Notícias](https://noticias.uol.com.br/); [Poder360](https://www.poder360.com.br/); [CNN Brasil](https://www.cnnbrasil.com.br/); [Nexo Jornal](https://www.nexojornal.com.br/); [Agência Pública](https://apublica.org/); [Brasil de Fato](https://www.brasildefato.com.br/)

**Governo principal:** [Presidência da República — Planalto](https://www.gov.br/planalto/)

**Universidades:** [Universidade de São Paulo](https://www.usp.br/); [Unicamp](https://www.unicamp.br/); [Universidade Federal do Rio de Janeiro](https://ufrj.br/); [Universidade Federal de Minas Gerais](https://ufmg.br/); [Universidade Estadual Paulista](https://www.unesp.br/)

| Tema | Cinco fontes |
|---|---|
| Geopolítica e relações internacionais | [Itamaraty](https://www.gov.br/mre/); [Agência Brasil](https://agenciabrasil.ebc.com.br/); [Folha de S.Paulo](https://www.folha.uol.com.br/); [Poder360](https://www.poder360.com.br/); [CNN Brasil](https://www.cnnbrasil.com.br/) |
| Política nacional | [Agência Brasil](https://agenciabrasil.ebc.com.br/); [g1](https://g1.globo.com/); [Folha de S.Paulo](https://www.folha.uol.com.br/); [Poder360](https://www.poder360.com.br/); [Agência Pública](https://apublica.org/) |
| Ciência | [Agência FAPESP](https://agencia.fapesp.br/); [Pesquisa FAPESP](https://revistapesquisa.fapesp.br/); [Universidade de São Paulo](https://www.usp.br/); [Unicamp](https://www.unicamp.br/); [Sociedade Brasileira para o Progresso da Ciência](https://portal.sbpcnet.org.br/) |
| Física | [Centro Brasileiro de Pesquisas Físicas](https://www.gov.br/cbpf/); [Centro Nacional de Pesquisa em Energia e Materiais](https://cnpem.br/); [Pesquisa FAPESP](https://revistapesquisa.fapesp.br/); [Universidade de São Paulo](https://www.usp.br/); [Unicamp](https://www.unicamp.br/) |
| Astronomia | [INPE](https://www.gov.br/inpe/); [Observatório Nacional](https://www.gov.br/observatorio/); [Agência Espacial Brasileira](https://www.gov.br/aeb/); [Universidade de São Paulo](https://www.usp.br/); [Pesquisa FAPESP](https://revistapesquisa.fapesp.br/) |
| Tecnologia e inteligência artificial | [Tecnoblog](https://tecnoblog.net/); [Canaltech](https://canaltech.com.br/); [TecMundo](https://www.tecmundo.com.br/); [MacMagazine](https://macmagazine.com.br/); [Olhar Digital](https://olhardigital.com.br/) |
| Economia e comércio | [Valor Econômico](https://valor.globo.com/); [InfoMoney](https://www.infomoney.com.br/); [IBGE](https://www.ibge.gov.br/); [Agência Brasil](https://agenciabrasil.ebc.com.br/); [Folha de S.Paulo](https://www.folha.uol.com.br/) |
| Energia, clima e meio ambiente | [INPE](https://www.gov.br/inpe/); [O Eco](https://oeco.org.br/); [Agência Pública](https://apublica.org/); [ClimaInfo](https://climainfo.org.br/); [agência epbr](https://epbr.com.br/) |
| Defesa e segurança | [DefesaNet](https://www.defesanet.com.br/); [Defesa Aérea & Naval](https://www.defesaaereanaval.com.br/); [Poder Naval](https://www.naval.com.br/); [Agência Brasil](https://agenciabrasil.ebc.com.br/); [Ministério da Defesa do Brasil](https://www.gov.br/defesa/) |
| Saúde e pesquisa médica | [Fundação Oswaldo Cruz](https://agencia.fiocruz.br/); [Instituto Butantan](https://butantan.gov.br/); [Ministério da Saúde do Brasil](https://www.gov.br/saude/); [Agência Brasil](https://agenciabrasil.ebc.com.br/); [Pesquisa FAPESP](https://revistapesquisa.fapesp.br/) |

## Estados Unidos

51 fontes únicas.

**Veículos jornalísticos:** [Associated Press](https://apnews.com/); [NPR](https://www.npr.org/); [The New York Times](https://www.nytimes.com/); [The Washington Post](https://www.washingtonpost.com/); [The Wall Street Journal](https://www.wsj.com/); [CNN](https://www.cnn.com/); [Fox News](https://www.foxnews.com/); [ProPublica](https://www.propublica.org/); [Ars Technica](https://arstechnica.com/); [The Verge](https://www.theverge.com/)

**Governo principal:** [Casa Branca](https://www.whitehouse.gov/)

**Universidades:** [Massachusetts Institute of Technology](https://www.mit.edu/); [Harvard University](https://www.harvard.edu/); [Stanford University](https://news.stanford.edu/); [Princeton University](https://www.princeton.edu/); [California Institute of Technology](https://www.caltech.edu/)

| Tema | Cinco fontes |
|---|---|
| Geopolítica e relações internacionais | [Associated Press](https://apnews.com/); [NPR](https://www.npr.org/); [Foreign Affairs](https://www.foreignaffairs.com/); [Foreign Policy](https://foreignpolicy.com/); [Departamento de Estado](https://www.state.gov/) |
| Política nacional | [Associated Press](https://apnews.com/); [NPR](https://www.npr.org/); [The New York Times](https://www.nytimes.com/); [The Washington Post](https://www.washingtonpost.com/); [Politico](https://www.politico.com/) |
| Ciência | [Science News](https://www.sciencenews.org/); [Science — AAAS](https://www.science.org/); [Scientific American](https://www.scientificamerican.com/); [Massachusetts Institute of Technology](https://www.mit.edu/); [Harvard University](https://www.harvard.edu/) |
| Física | [Physics — American Physical Society](https://physics.aps.org/); [Physics Today — AIP](https://pubs.aip.org/); [SLAC National Accelerator Laboratory](https://www6.slac.stanford.edu/); [Fermilab](https://www.fnal.gov/); [California Institute of Technology](https://www.caltech.edu/) |
| Astronomia | [NASA](https://www.nasa.gov/); [Space.com](https://www.space.com/); [Astronomy Magazine](https://www.astronomy.com/); [Sky & Telescope](https://skyandtelescope.org/); [California Institute of Technology](https://www.caltech.edu/) |
| Tecnologia e inteligência artificial | [Ars Technica](https://arstechnica.com/); [The Verge](https://www.theverge.com/); [WIRED](https://www.wired.com/); [TechCrunch](https://techcrunch.com/); [Engadget](https://www.engadget.com/) |
| Economia e comércio | [The Wall Street Journal](https://www.wsj.com/); [Bloomberg](https://www.bloomberg.com/); [CNBC](https://www.cnbc.com/); [Bureau of Labor Statistics](https://www.bls.gov/); [Federal Reserve](https://www.federalreserve.gov/) |
| Energia, clima e meio ambiente | [NOAA](https://www.noaa.gov/); [Inside Climate News](https://insideclimatenews.org/); [Grist](https://grist.org/); [Energy Information Administration](https://www.eia.gov/); [NASA](https://www.nasa.gov/) |
| Defesa e segurança | [Defense News](https://www.defensenews.com/); [Breaking Defense](https://breakingdefense.com/); [Defense One](https://www.defenseone.com/); [Stars and Stripes](https://www.stripes.com/); [Departamento de Defesa dos EUA](https://www.defense.gov/) |
| Saúde e pesquisa médica | [National Institutes of Health](https://www.nih.gov/); [Centers for Disease Control and Prevention](https://www.cdc.gov/); [KFF Health News](https://kffhealthnews.org/); [STAT](https://www.statnews.com/); [Harvard University](https://www.harvard.edu/) |

## China

38 fontes únicas.

**Veículos jornalísticos:** [Xinhua](https://english.news.cn/); [People’s Daily](http://en.people.cn/); [China Daily](https://www.chinadaily.com.cn/); [CGTN](https://www.cgtn.com/); [Global Times](https://www.globaltimes.cn/); [China News Service / ECNS](https://www.ecns.cn/); [Caixin Global](https://www.caixinglobal.com/); [Sixth Tone](https://www.sixthtone.com/); [Yicai Global](https://www.yicaiglobal.com/); [South China Morning Post](https://www.scmp.com/)

**Governo principal:** [Conselho de Estado da China](https://english.www.gov.cn/)

**Universidades:** [Tsinghua University](https://www.tsinghua.edu.cn/en/); [Peking University](https://english.pku.edu.cn/); [Zhejiang University](https://www.zju.edu.cn/); [Shanghai Jiao Tong University](https://en.sjtu.edu.cn/); [Fudan University](https://www.fudan.edu.cn/)

| Tema | Cinco fontes |
|---|---|
| Geopolítica e relações internacionais | [Xinhua](https://english.news.cn/); [People’s Daily](http://en.people.cn/); [CGTN](https://www.cgtn.com/); [South China Morning Post](https://www.scmp.com/); [Ministério das Relações Exteriores da China](https://www.fmprc.gov.cn/eng/) |
| Política nacional | [Xinhua](https://english.news.cn/); [People’s Daily](http://en.people.cn/); [China Daily](https://www.chinadaily.com.cn/); [Caixin Global](https://www.caixinglobal.com/); [CGTN](https://www.cgtn.com/) |
| Ciência | [Chinese Academy of Sciences](https://english.cas.cn/); [ScienceNet China](https://news.sciencenet.cn/); [Science and Technology Daily](https://www.stdaily.com/); [Tsinghua University](https://www.tsinghua.edu.cn/en/); [Peking University](https://english.pku.edu.cn/) |
| Física | [Institute of High Energy Physics — CAS](https://english.ihep.cas.cn/); [Institute of Physics — CAS](https://english.iop.cas.cn/); [Fudan University](https://www.fudan.edu.cn/); [ScienceNet China](https://news.sciencenet.cn/); [Chinese Academy of Sciences](https://english.cas.cn/) |
| Astronomia | [Chinese Academy of Sciences](https://english.cas.cn/); [National Astronomical Observatories — CAS](https://english.nao.cas.cn/); [China National Space Administration](https://www.cnsa.gov.cn/); [Purple Mountain Observatory — CAS](https://english.pmo.cas.cn/); [Xinhua](https://english.news.cn/) |
| Tecnologia e inteligência artificial | [36Kr](https://36kr.com/); [IT Home](https://www.ithome.com/); [GeekPark](https://www.geekpark.net/); [PingWest](https://en.pingwest.com/); [TechNode](https://technode.com/) |
| Economia e comércio | [Caixin Global](https://www.caixinglobal.com/); [Yicai Global](https://www.yicaiglobal.com/); [South China Morning Post](https://www.scmp.com/); [National Bureau of Statistics of China](https://www.stats.gov.cn/english/); [China Daily](https://www.chinadaily.com.cn/) |
| Energia, clima e meio ambiente | [China Meteorological Administration](https://www.cma.gov.cn/); [Ministério da Ecologia e Meio Ambiente da China](https://english.mee.gov.cn/); [National Energy Administration](https://www.nea.gov.cn/); [Chinese Academy of Sciences](https://english.cas.cn/); [China Daily](https://www.chinadaily.com.cn/) |
| Defesa e segurança | [Ministério da Defesa da China](http://eng.mod.gov.cn/); [China Military Online](http://eng.chinamil.com.cn/); [Xinhua](https://english.news.cn/); [CGTN](https://www.cgtn.com/); [South China Morning Post](https://www.scmp.com/) |
| Saúde e pesquisa médica | [National Health Commission](http://en.nhc.gov.cn/); [Chinese Center for Disease Control and Prevention](https://en.chinacdc.cn/); [Chinese Academy of Sciences](https://english.cas.cn/); [Fudan University](https://www.fudan.edu.cn/); [Peking University](https://english.pku.edu.cn/) |

## Rússia

38 fontes únicas.

**Veículos jornalísticos:** [TASS](https://tass.com/); [RIA Novosti](https://ria.ru/); [Interfax](https://www.interfax.ru/); [RBC](https://www.rbc.ru/); [Kommersant](https://www.kommersant.ru/); [Vedomosti](https://www.vedomosti.ru/); [Rossiyskaya Gazeta](https://rg.ru/); [RT](https://www.rt.com/); [The Moscow Times](https://www.themoscowtimes.com/); [Meduza](https://meduza.io/)

**Governo principal:** [Presidência da Rússia — Kremlin](https://en.kremlin.ru/)

**Universidades:** [Universidade Estatal de Moscou](https://www.msu.ru/); [ITMO University](https://en.itmo.ru/); [Saint Petersburg State University](https://english.spbu.ru/); [Moscow Institute of Physics and Technology](https://mipt.ru/); [HSE University](https://www.hse.ru/)

| Tema | Cinco fontes |
|---|---|
| Geopolítica e relações internacionais | [TASS](https://tass.com/); [Interfax](https://www.interfax.ru/); [Kommersant](https://www.kommersant.ru/); [Ministério das Relações Exteriores da Rússia](https://mid.ru/en/); [Meduza](https://meduza.io/) |
| Política nacional | [TASS](https://tass.com/); [RIA Novosti](https://ria.ru/); [RBC](https://www.rbc.ru/); [Meduza](https://meduza.io/); [The Moscow Times](https://www.themoscowtimes.com/) |
| Ciência | [N + 1](https://nplus1.ru/); [Indicator](https://indicator.ru/); [Elementy](https://elementy.ru/); [Academia Russa de Ciências](https://www.ras.ru/); [Universidade Estatal de Moscou](https://www.msu.ru/) |
| Física | [Joint Institute for Nuclear Research — Dubna](https://www.jinr.ru/); [Moscow Institute of Physics and Technology](https://mipt.ru/); [Elementy](https://elementy.ru/); [Academia Russa de Ciências](https://www.ras.ru/); [Universidade Estatal de Moscou](https://www.msu.ru/) |
| Astronomia | [Roscosmos](https://www.roscosmos.ru/); [Space Research Institute — RAS](https://iki.cosmos.ru/); [Institute of Astronomy — RAS](https://www.inasan.ru/); [N + 1](https://nplus1.ru/); [Academia Russa de Ciências](https://www.ras.ru/) |
| Tecnologia e inteligência artificial | [3DNews](https://3dnews.ru/); [iXBT](https://www.ixbt.com/); [CNews](https://www.cnews.ru/); [Habr](https://habr.com/); [N + 1](https://nplus1.ru/) |
| Economia e comércio | [RBC](https://www.rbc.ru/); [Vedomosti](https://www.vedomosti.ru/); [Kommersant](https://www.kommersant.ru/); [Banco da Rússia](https://www.cbr.ru/eng/); [Interfax](https://www.interfax.ru/) |
| Energia, clima e meio ambiente | [Roshydromet](https://www.meteorf.gov.ru/); [Hydrometeorological Centre of Russia](https://meteoinfo.ru/); [Ministério da Energia da Rússia](https://minenergo.gov.ru/); [N + 1](https://nplus1.ru/); [Academia Russa de Ciências](https://www.ras.ru/) |
| Defesa e segurança | [TASS](https://tass.com/); [Interfax](https://www.interfax.ru/); [Kommersant](https://www.kommersant.ru/); [Ministério da Defesa da Rússia](https://mil.ru/); [Krasnaya Zvezda](https://redstar.ru/) |
| Saúde e pesquisa médica | [Ministério da Saúde da Rússia](https://minzdrav.gov.ru/); [Rospotrebnadzor](https://www.rospotrebnadzor.ru/); [Medvestnik](https://medvestnik.ru/); [N + 1](https://nplus1.ru/); [Indicator](https://indicator.ru/) |

## Limites de integração

A verificação inicial acessou apenas canais e metadados, sem artigos nem modelo: 117 canais apresentaram candidatos, 12 responderam sem itens elegíveis e 41 apresentaram bloqueio, limite ou falha. Esses números são da verificação inicial, não garantem extração de texto nem cobertura por dia; ajustes posteriores de metadados não foram retestados em rede. A coleta no aplicativo registra o estado efetivo de cada fonte. Não foram contornados robots.txt ou controles de acesso.

Cadastrar uma fonte não garante acesso automático a todas as notícias. Para tecnologia brasileira, Tecnoblog, MacMagazine e Olhar Digital retornaram itens com datas nessa verificação; Canaltech bloqueou o leitor e TecMundo exigiu ajuste de domínio dos links.

| Fonte | Canal | Verificação inicial |
|---|---|---|
| Agência Brasil | [feed](https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml) | candidatos |
| g1 | [feed](https://g1.globo.com/rss/g1/) | candidatos |
| Folha de S.Paulo | [feed](https://feeds.folha.uol.com.br/emcimadahora/rss091.xml) | sem_itens |
| Estadão | [page](https://www.estadao.com.br/) | candidatos |
| UOL Notícias | [feed](https://rss.uol.com.br/feed/noticias.xml) | candidatos |
| Poder360 | [feed](https://www.poder360.com.br/feed/) | candidatos |
| CNN Brasil | [feed](https://www.cnnbrasil.com.br/feed/) | indisponivel: HTTP 403; conteúdo não recuperado. |
| Nexo Jornal | [page](https://www.nexojornal.com.br/) | sem_itens |
| Agência Pública | [feed](https://apublica.org/feed/) | candidatos |
| Brasil de Fato | [feed](https://www.brasildefato.com.br/feed/) | candidatos |
| Associated Press | [page](https://apnews.com/) | candidatos |
| NPR | [feed](https://feeds.npr.org/1001/rss.xml) | candidatos |
| The New York Times | [feed](https://rss.nytimes.com/services/xml/rss/nyt/World.xml) | candidatos |
| The Washington Post | [feed](https://feeds.washingtonpost.com/rss/world) | candidatos |
| The Wall Street Journal | [feed](https://feeds.content.dowjones.io/public/rss/RSSWorldNews) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| CNN | [page](https://www.cnn.com/) | candidatos |
| Fox News | [feed](https://moxie.foxnews.com/google-publisher/world.xml) | candidatos |
| ProPublica | [feed](https://www.propublica.org/feeds/propublica/main) | candidatos |
| Ars Technica | [feed](https://feeds.arstechnica.com/arstechnica/index) | candidatos |
| The Verge | [feed](https://www.theverge.com/rss/index.xml) | candidatos |
| Xinhua | [page](https://english.news.cn/) | candidatos |
| People’s Daily | [feed](http://en.people.cn/rss/World.xml) | sem_itens |
| China Daily | [page](https://www.chinadaily.com.cn/) | candidatos |
| CGTN | [page](https://www.cgtn.com/) | candidatos |
| Global Times | [page](https://www.globaltimes.cn/) | candidatos |
| China News Service / ECNS | [page](https://www.ecns.cn/) | candidatos |
| Caixin Global | [page](https://www.caixinglobal.com/) | candidatos |
| Sixth Tone | [page](https://www.sixthtone.com/) | candidatos |
| Yicai Global | [page](https://www.yicaiglobal.com/) | candidatos |
| South China Morning Post | [feed](https://www.scmp.com/rss/91/feed) | indisponivel: Falha de leitura (TimeoutError); conteúdo não recuperado. |
| TASS | [feed](https://tass.com/rss/v2.xml) | candidatos |
| RIA Novosti | [feed](https://ria.ru/export/rss2/archive/index.xml) | candidatos |
| Interfax | [feed](https://www.interfax.ru/rss.asp) | candidatos |
| RBC | [feed](https://rssexport.rbc.ru/rbcnews/news/30/full.rss) | candidatos |
| Kommersant | [feed](https://www.kommersant.ru/RSS/news.xml) | indisponivel: Leitura não permitida pelo robots.txt da fonte. |
| Vedomosti | [feed](https://www.vedomosti.ru/rss/news.xml) | candidatos |
| Rossiyskaya Gazeta | [feed](https://rg.ru/xml/index.xml) | candidatos |
| RT | [feed](https://www.rt.com/rss/) | candidatos |
| The Moscow Times | [feed](https://www.themoscowtimes.com/rss/news) | candidatos |
| Meduza | [feed](https://meduza.io/rss2/en/all) | candidatos |
| Itamaraty | [page](https://www.gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa) | candidatos |
| IBGE | [page](https://agenciadenoticias.ibge.gov.br/agencia-noticias.html) | candidatos |
| INPE | [page](https://www.gov.br/inpe/pt-br/assuntos/ultimas-noticias) | candidatos |
| Universidade de São Paulo | [feed](https://jornal.usp.br/feed/) | candidatos |
| Unicamp | [page](https://www.unicamp.br/) | candidatos |
| Departamento de Estado | [page](https://www.state.gov/press-releases/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Bureau of Labor Statistics | [feed](https://www.bls.gov/feed/bls_latest.rss) | candidatos |
| NASA | [feed](https://www.nasa.gov/feed/) | candidatos |
| Massachusetts Institute of Technology | [feed](https://news.mit.edu/rss/feed) | candidatos |
| Harvard University | [feed](https://news.harvard.edu/gazette/feed/) | candidatos |
| Ministério das Relações Exteriores da China | [page](https://www.fmprc.gov.cn/eng/xw/fyrbt/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| National Bureau of Statistics of China | [page](https://www.stats.gov.cn/english/PressRelease/) | candidatos |
| Chinese Academy of Sciences | [page](https://english.cas.cn/newsroom/research_news/) | indisponivel: HTTP 403; conteúdo não recuperado. |
| Tsinghua University | [page](https://www.tsinghua.edu.cn/en/News/LATEST_NEWS.htm) | candidatos |
| Peking University | [page](https://newsen.pku.edu.cn/newscenter.html) | candidatos |
| Ministério das Relações Exteriores da Rússia | [page](https://mid.ru/en/foreign_policy/news/) | candidatos |
| Banco da Rússia | [feed](https://www.cbr.ru/rss/RssPress) | candidatos |
| Academia Russa de Ciências | [page](https://www.ras.ru/news.aspx) | candidatos |
| Universidade Estatal de Moscou | [page](https://www.msu.ru/news/) | sem_itens |
| ITMO University | [page](https://news.itmo.ru/en/) | candidatos |
| Presidência da República — Planalto | [page](https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/noticias) | candidatos |
| Universidade Federal do Rio de Janeiro | [feed](https://conexao.ufrj.br/feed/) | candidatos |
| Universidade Federal de Minas Gerais | [page](https://ufmg.br/comunicacao/noticias) | candidatos |
| Universidade Estadual Paulista | [feed](https://jornal.unesp.br/feed/) | candidatos |
| Tecnoblog | [feed](https://tecnoblog.net/feed/) | candidatos |
| Canaltech | [feed](https://canaltech.com.br/rss/) | indisponivel: Leitura não permitida pelo robots.txt da fonte. |
| TecMundo | [feed](https://rss.tecmundo.com.br/feed) | sem_itens |
| MacMagazine | [feed](https://macmagazine.com.br/feed/) | candidatos |
| Olhar Digital | [feed](https://olhardigital.com.br/feed/) | candidatos |
| Agência FAPESP | [page](https://agencia.fapesp.br/) | candidatos |
| Pesquisa FAPESP | [feed](https://revistapesquisa.fapesp.br/feed/) | indisponivel: A fonte exige intervalo superior ao limite desta coleta; coleta adiada. |
| Sociedade Brasileira para o Progresso da Ciência | [feed](https://portal.sbpcnet.org.br/feed/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Centro Brasileiro de Pesquisas Físicas | [page](https://www.gov.br/cbpf/pt-br/assuntos/noticias) | sem_itens |
| Centro Nacional de Pesquisa em Energia e Materiais | [feed](https://cnpem.br/feed/) | candidatos |
| Observatório Nacional | [page](https://www.gov.br/observatorio/pt-br/assuntos/noticias) | candidatos |
| Agência Espacial Brasileira | [page](https://www.gov.br/aeb/pt-br/assuntos/noticias) | candidatos |
| Valor Econômico | [page](https://valor.globo.com/) | candidatos |
| InfoMoney | [feed](https://www.infomoney.com.br/feed/) | candidatos |
| O Eco | [feed](https://oeco.org.br/feed/) | candidatos |
| ClimaInfo | [feed](https://climainfo.org.br/feed/) | candidatos |
| agência epbr | [feed](https://epbr.com.br/feed/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| DefesaNet | [feed](https://www.defesanet.com.br/feed/) | candidatos |
| Defesa Aérea & Naval | [feed](https://www.defesaaereanaval.com.br/feed) | candidatos |
| Poder Naval | [feed](https://www.naval.com.br/blog/feed/) | candidatos |
| Ministério da Defesa do Brasil | [page](https://www.gov.br/defesa/pt-br/centrais-de-conteudo/noticias) | candidatos |
| Fundação Oswaldo Cruz | [page](https://agencia.fiocruz.br/noticias) | candidatos |
| Instituto Butantan | [page](https://butantan.gov.br/noticias) | indisponivel: HTTP 403; conteúdo não recuperado. |
| Ministério da Saúde do Brasil | [page](https://www.gov.br/saude/pt-br/assuntos/noticias) | candidatos |
| Casa Branca | [page](https://www.whitehouse.gov/news/) | candidatos |
| Stanford University | [page](https://news.stanford.edu/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Princeton University | [page](https://www.princeton.edu/news) | candidatos |
| California Institute of Technology | [page](https://www.caltech.edu/about/news) | indisponivel: HTTP 403; conteúdo não recuperado. |
| Foreign Affairs | [page](https://www.foreignaffairs.com/) | candidatos |
| Foreign Policy | [feed](https://foreignpolicy.com/feed/) | candidatos |
| Politico | [feed](https://www.politico.com/rss/politicopicks.xml) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Science News | [feed](https://www.sciencenews.org/feed) | candidatos |
| Science — AAAS | [page](https://www.science.org/news) | indisponivel: HTTP 403; conteúdo não recuperado. |
| Scientific American | [page](https://www.scientificamerican.com/) | candidatos |
| Physics — American Physical Society | [page](https://physics.aps.org/) | indisponivel: HTTP 403; conteúdo não recuperado. |
| Physics Today — AIP | [page](https://pubs.aip.org/physicstoday) | indisponivel: HTTP 403; conteúdo não recuperado. |
| SLAC National Accelerator Laboratory | [page](https://www6.slac.stanford.edu/news) | candidatos |
| Fermilab | [feed](https://news.fnal.gov/feed/) | candidatos |
| Space.com | [feed](https://www.space.com/feeds/all) | candidatos |
| Astronomy Magazine | [feed](https://www.astronomy.com/feed/) | candidatos |
| Sky & Telescope | [feed](https://skyandtelescope.org/feed/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| WIRED | [feed](https://www.wired.com/feed/rss) | candidatos |
| TechCrunch | [feed](https://techcrunch.com/feed/) | candidatos |
| Engadget | [feed](https://www.engadget.com/rss.xml) | candidatos |
| Bloomberg | [feed](https://feeds.bloomberg.com/markets/news.rss) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| CNBC | [feed](https://www.cnbc.com/id/100003114/device/rss/rss.html) | candidatos |
| Federal Reserve | [feed](https://www.federalreserve.gov/feeds/press_all.xml) | candidatos |
| NOAA | [page](https://www.noaa.gov/news) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Inside Climate News | [feed](https://insideclimatenews.org/feed/) | candidatos |
| Grist | [feed](https://grist.org/feed/) | candidatos |
| Energy Information Administration | [page](https://www.eia.gov/todayinenergy/) | candidatos |
| Defense News | [page](https://www.defensenews.com/) | candidatos |
| Breaking Defense | [feed](https://breakingdefense.com/feed/) | candidatos |
| Defense One | [page](https://www.defenseone.com/) | candidatos |
| Stars and Stripes | [page](https://www.stripes.com/) | candidatos |
| Departamento de Defesa dos EUA | [page](https://www.defense.gov/News/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| National Institutes of Health | [page](https://www.nih.gov/news-events/news-releases) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Centers for Disease Control and Prevention | [page](https://www.cdc.gov/media/) | candidatos |
| KFF Health News | [feed](https://kffhealthnews.org/feed/) | candidatos |
| STAT | [feed](https://www.statnews.com/feed/) | candidatos |
| Conselho de Estado da China | [page](https://english.www.gov.cn/news/) | candidatos |
| Zhejiang University | [page](https://www.zju.edu.cn/english/) | candidatos |
| Shanghai Jiao Tong University | [page](https://en.sjtu.edu.cn/news) | indisponivel: Redirecionamento ou domínio fora da fonte cadastrada; não seguido. |
| Fudan University | [page](https://www.fudan.edu.cn/en/) | candidatos |
| ScienceNet China | [page](https://news.sciencenet.cn/) | candidatos |
| Science and Technology Daily | [page](https://www.stdaily.com/) | candidatos |
| Institute of High Energy Physics — CAS | [page](https://english.ihep.cas.cn/nw/) | candidatos |
| Institute of Physics — CAS | [page](https://english.iop.cas.cn/) | candidatos |
| National Astronomical Observatories — CAS | [page](https://english.nao.cas.cn/) | candidatos |
| China National Space Administration | [page](https://www.cnsa.gov.cn/english/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Purple Mountain Observatory — CAS | [page](https://english.pmo.cas.cn/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| 36Kr | [feed](https://36kr.com/feed) | sem_itens |
| IT Home | [feed](https://www.ithome.com/rss/) | candidatos |
| GeekPark | [page](https://www.geekpark.net/) | indisponivel: HTTP 403; conteúdo não recuperado. |
| PingWest | [page](https://en.pingwest.com/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| TechNode | [feed](https://technode.com/feed/) | indisponivel: Documento excede limite de 8 MB do piloto. |
| China Meteorological Administration | [page](https://www.cma.gov.cn/en2014/) | sem_itens |
| Ministério da Ecologia e Meio Ambiente da China | [page](https://english.mee.gov.cn/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| National Energy Administration | [page](https://www.nea.gov.cn/) | candidatos |
| Ministério da Defesa da China | [page](http://eng.mod.gov.cn/) | candidatos |
| China Military Online | [page](http://eng.chinamil.com.cn/) | candidatos |
| National Health Commission | [page](http://en.nhc.gov.cn/) | indisponivel: HTTP 502; conteúdo não recuperado. |
| Chinese Center for Disease Control and Prevention | [page](https://en.chinacdc.cn/) | candidatos |
| Presidência da Rússia — Kremlin | [page](https://en.kremlin.ru/events/president/news) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Saint Petersburg State University | [page](https://english.spbu.ru/news-events/news) | candidatos |
| Moscow Institute of Physics and Technology | [page](https://mipt.ru/news/) | sem_itens |
| HSE University | [page](https://www.hse.ru/en/news/) | candidatos |
| N + 1 | [feed](https://nplus1.ru/rss) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Indicator | [page](https://indicator.ru/) | sem_itens |
| Elementy | [feed](https://elementy.ru/rss/news) | indisponivel: A fonte exige intervalo superior ao limite desta coleta; coleta adiada. |
| Joint Institute for Nuclear Research — Dubna | [page](https://www.jinr.ru/posts/category/news/) | indisponivel: HTTP 404; conteúdo não recuperado. |
| Roscosmos | [page](https://www.roscosmos.ru/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Space Research Institute — RAS | [page](https://iki.cosmos.ru/news) | candidatos |
| Institute of Astronomy — RAS | [page](https://www.inasan.ru/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| 3DNews | [feed](https://3dnews.ru/news/rss/) | candidatos |
| iXBT | [feed](https://www.ixbt.com/export/news.rss) | candidatos |
| CNews | [feed](https://www.cnews.ru/inc/rss/news.xml) | candidatos |
| Habr | [feed](https://habr.com/ru/rss/news/) | candidatos |
| Roshydromet | [page](https://www.meteorf.gov.ru/) | candidatos |
| Hydrometeorological Centre of Russia | [page](https://meteoinfo.ru/novosti) | sem_itens |
| Ministério da Energia da Rússia | [page](https://minenergo.gov.ru/) | sem_itens |
| Ministério da Defesa da Rússia | [page](https://mil.ru/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Krasnaya Zvezda | [feed](https://redstar.ru/feed/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Ministério da Saúde da Rússia | [page](https://minzdrav.gov.ru/news) | candidatos |
| Rospotrebnadzor | [page](https://www.rospotrebnadzor.ru/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
| Medvestnik | [page](https://medvestnik.ru/) | indisponivel: Não foi possível verificar robots.txt; coleta adiada. |
