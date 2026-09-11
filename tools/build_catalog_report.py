import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.catalog import COUNTRIES,SOURCES
ROOT=Path(__file__).resolve().parents[1]
report=json.loads((ROOT/'docs/source-audit.json').read_text(encoding='utf-8'))
checks={s['source_id']:s for s in report['sources']}
labels={'disponivel':'Texto recuperado','parcial':'Parcial','indisponivel':'Indisponível','desatualizado':'Desatualizado'}
lines=['# Catálogo e cobertura do piloto','',f"Teste registrado em {report['checked_at']} (UTC).",'',
 'São 10 veículos jornalísticos, duas universidades e três instituições por país. A escolha combina cobertura geral, ciência/tecnologia, economia e investigações; inclui diferentes vínculos institucionais e formatos. Não é ranking nem amostra representativa de toda a opinião pública. As informações de vínculo são descrições editoriais do catálogo, a serem revistas com mudanças de propriedade ou operação.','',
 'Os testes acessaram os canais e até um artigo por fonte, sem OpenAI. Texto recuperado não significa cobertura integral; parcial pode ser apenas resumo distribuído ou metadados. A consulta por período exclui publicação sem data verificável. Cada URL é um canal concreto usado pelo conector, não promessa de acesso. O aplicativo atualiza o estado por coleta.','',
 'RSS/Atom é priorizado por oferecer links e datas estruturadas. Páginas usam descoberta limitada de links, com preferência pelo corpo editorial. A versão anterior do feed China Daily era de 2017; a coleta passou para a página oficial atual. Fontes que bloqueiam acesso ou não oferecem itens elegíveis permanecem claramente sinalizadas.','',
 '## Fundamentos e referências institucionais','',
 '- [Agência Brasil / relatório da EBC sobre RSS](https://acessoainformacao.ebc.com.br/participacao-social/ouvidoria/relatorios/relatorios-da-ouvidoria/2020-04.pdf): documenta o canal de últimas notícias.','- [Sixth Tone: apresentação institucional](https://m.sixthtone.com/about-us): informa vínculo com Shanghai United Media Group.','- [SCMP: apresentação institucional](https://corp.scmp.com/about-us/): sede e foco editorial em Hong Kong.','- [Meduza: apresentação institucional](https://meduza.io/en/pages/about) e [declaração sobre a operação na Letônia](https://meduza.io/en/feature/2023/09/13/even-in-europe-we-are-not-safe).','- [The Moscow Times: apresentação](https://www.themoscowtimes.com/page/moscow-times): veículo independente de origem russa.','- Universidades: USP e Unicamp; MIT e Harvard; Tsinghua e Peking; Universidade Estatal de Moscou e ITMO. Seleção inicial com pesquisa multidisciplinar e tecnológica, complementada pelas instituições científicas públicas; não representa uma lista exaustiva das principais universidades.','',
 'País é o contexto de origem editorial da fonte, não nacionalidade da empresa pesquisada nem país da notícia. SCMP é de Hong Kong; Meduza e Moscow Times têm origem russa e operação no exterior. Fontes estatais/oficiais são evidência de sua própria posição. Folha e UOL têm vínculo de grupo: isso é informado e não se presume independência.','']
for code,country in COUNTRIES.items():
    lines.extend(['## '+country,'','| Fonte / vínculo | Tipo | Canal | Resultado do teste |','|---|---|---|---|'])
    for s in [s for s in SOURCES if s['country']==code]:
        check=checks.get(s['id'],{})
        detail=check.get('detail',{})
        kind={'jornalismo':'Jornalismo','universidade':'Universidade','instituicao':'Instituição'}[s['kind']]
        message=detail.get('message','Não testada.').replace('|','/')
        lines.append(f"| [{s['name']}]({s['home']}) — {s['affiliation']} | {kind} | [{s['connector']}]({s['channel']}) | **{labels.get(check.get('status'),'Não testada')}**. {message} |")
    lines.append('')
lines.extend(['## Como ler o resultado','',
 'O JSON acompanhante contém contagem de candidatos, leituras, falhas por URL, janela temporal do feed quando disponível e data do teste. Uma falha em uma fonte não impede apresentar conteúdo das outras. Conteúdo parcial nunca autoriza inferir o trecho não lido. As verificações não contornaram paywalls, CAPTCHAs ou restrições de acesso.','',
 'Artigos científicos são ligados aos estudos/dados quando esses links constam da notícia. Preprints são identificados pelo endereço da plataforma. A revisão por pares não é presumida a partir de um comunicado ou do nome de um periódico.'])
(ROOT/'docs/CATALOGO.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Catálogo documentado:',len(SOURCES),'fontes.')
