# Validação da entrega · piloto 0.1

Validado no Windows em 7 de setembro de 2026 (horário de São Paulo; registros técnicos também usam UTC).

## Testes realizados

- **17 testes de backend passaram** na instalação definitiva em `C:\ObservatorioFontes`, com banco/pastas temporários isolados. Cobrem: catálogo 10+5 por país; datas editoriais/fusos e intervalo inclusivo; palavra-chave sem expansão de países; temas; exclusão de data desconhecida; deduplicação; revisão e preservação de texto após releitura parcial; instantâneo de consulta; RSS/Atom; URLs fora da fonte; paywall; falhas individuais; pares relacionados/origem comum; proteção de sessão/Origin; histórico; exportação; backup e restauração; rejeição de referências inventadas; ausência de chave; versões de análise e cache de áudio; distribuição do limite de resultados entre as fontes.
- **Três testes de interface passaram**: globo com geometria real, seleção de países sem alteração pela palavra Samsung, data única/atalho Ontem, salvamento deliberado e navegação nas três páginas. Fixtures identificadas como sintéticas, sem chamadas pagas.
- **Compilação TypeScript + Vite concluída.** A pasta `app/static` contém a interface pronta. Não há dependência de Node para executar o piloto.
- **Navegador real:** páginas Explorar/Histórico/Configurações abertas; globo girado para Ásia e China selecionada diretamente no polígono; quatro países selecionados; calendário alterado; consulta real para 07/09/2026; resultado com 58 documentos BR, 34 US, 16 CN e 92 RU dentro do limite de 200; consulta salva e reaberta; documento original aberto com autoria, datas e revisões; catálogo com 60 fontes; backup completo criado pela interface.
- **Inicialização local:** Python do ambiente virtual instalado em `C:\ObservatorioFontes`; resposta de saúde local e interface verificadas em `127.0.0.1:8765`. Nenhum serviço público, túnel, Docker ou banco separado.
- **Acervo real de validação:** 1.578 documentos e 2.941 revisões/observações preservadas após duas rodadas limitadas de coleta. Há documentos completos, resumos de feed e metadados. Contagens podem mudar em novas coletas. Nenhuma fixture sintética entrou nesse acervo.

## Coleta real por fonte

A rodada documentada testou os **60 canais** e até uma leitura de artigo por fonte. Resultado: **38 com texto recuperado, 13 parciais e nove indisponíveis**. A condição de cada fonte pode mudar; consulte a página Configurações e o arquivo `source-audit.json` com a data de cada teste.

“Texto recuperado” não significa canal integralmente coberto. Algumas páginas não informam data verificável e ficam fora das consultas temporais. Feed recente não é arquivo histórico. Os testes respeitaram bloqueios e robots.txt. Detalhes, URLs e fundamentos estão em `CATALOGO.md`.

## O que foi simulado e o que ainda depende da sua conta

**Não houve chamada real paga à OpenAI. Nenhuma API key foi fornecida.** O armazenamento/reuso de análises, validação de citações, versionamento e fluxo de áudio foram testados com respostas e bytes explicitamente sintéticos, somente nos testes. Os arquivos de áudio de teste não representam narração real e não fazem parte da distribuição/acervo.

Para usar análise e narração reais, cadastre a chave, escolha um modelo compatível e habilite o envio de textos em Configurações. A qualidade em PT-BR, a voz, a disponibilidade de modelo e a cobrança precisam ser verificadas com a conta do usuário. Não existe estimativa apresentada como garantia de gasto.

## Limitações do piloto

- Coleta limitada aos canais atuais e a até 10 artigos por fonte/execução. Sem busca universal, arquivo completo, login de assinante ou OCR.
- Classificação de tema/gênero/origem e agrupamento são heurísticos; não são detector de verdade ou de independência editorial. Relações textuais não estabelecem causalidade.
- Estudos/dados são vinculados quando citados; não há leitura automática de todos os estudos nem certificação automática de revisão por pares.
- Até 200 documentos por consulta, distribuídos alternadamente entre fontes com resultados. A IA tem limite adicional de entrada, visível antes da chamada.
- Testes e instalação executados em Windows; caminhos de execução em macOS/Linux foram documentados, mas não validados.
- O aplicativo é pessoal e local. Não foi projetado para exposição pública ou uso multiusuário.

Não foi publicado repositório remoto. O código e o pacote de distribuição excluem o acervo, chaves, logs pessoais, backups e áudios.


## Fluxo em etapas — 10/09/2026
Resumo com referências primeiro; cruzamentos e interpretações somente sob demanda. Esquemas menores por etapa, sem geração de roteiro ou endpoints de áudio. Acervo legado preservado. Quatro testes simulados passaram (separação, cache por etapa/resumo, streaming e interrupção por limite); TypeScript e build Vite passaram. Nenhuma inferência real executada. Reiniciar o aplicativo para carregar o backend atualizado.
