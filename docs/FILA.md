# Últimas duas mudanças — concluídas em 11/09/2026

- Imagens: removidas da coleta, da interface e da API de visualização. Arquivos e revisões antigos preservados.
- Síntese por país: trechos selecionados pela palavra-chave/tema com contexto próximo; agrupamento conservador de repetições dentro de cada país; até cinco pontos com identificadores de parágrafos convertidos em citações literais pelo programa. Links das matérias permanecem na consulta.
- Cache adaptado à síntese: reutilização quando o conjunto de revisões e trechos de um país, busca, modelo e instruções coincidem. Alterar os documentos de um país regenera sua síntese; não mistura resumos individuais antigos.
- Mantidos português para BR, inglês para os demais e cruzamentos sob demanda. Seleção de trechos é lexical, sem tradução automática ou novas etapas de IA.
- Verificação: cinco casos básicos simulados, com correção e repetição apenas do caso de limite dos trechos; TypeScript e build concluídos. Nenhuma busca ou inferência real executada. Desempenho e qualidade serão avaliados pelo usuário.

Ativação: Encerrar.cmd → Iniciar.cmd e recarregar. Para consultas já resumidas, usar Novo resumo para obter a nova síntese.

---
Histórico anterior (substituído pelas decisões acima):

# Próximas alterações — pendentes

Solicitadas pelo usuário; apenas registradas, sem implementação nesta etapa.

## 1. Remover o resumo ilustrado e as imagens
- Retirar a coleta de imagens, carregamento e apresentação do resumo ilustrado.
- Manter texto e referências como foco da leitura.
- Preservar documentos e análises existentes; remoção de arquivos antigos não está autorizada implicitamente.

## 2. Resumo mais relevante e rápido
Fluxo proposto: busca → trechos relevantes → agrupamento de repetições → síntese curta por país → validação de referências.
- Selecionar parágrafos relacionados à busca com contexto próximo, em vez de cortar apenas o início da matéria. Priorizar seleção sem chamada adicional de IA; informar limites em casos multilíngues.
- Agrupar matérias repetidas e reproduções, preservando fontes e links, sem tratar reprodução como confirmação independente.
- Aproveitar o cache existente por documento/revisão e adaptar sua reutilização à síntese por país e aos trechos selecionados.
- Numerar os parágrafos enviados; o modelo indica as referências e o programa recupera os trechos originais. Validar identificadores e atribuições; referência existente não garante sustentação semântica.
- Produzir síntese do assunto com até três a cinco pontos por país, conforme as evidências disponíveis, com referências por afirmação e lacunas explícitas.
- Brasil em português; demais fontes em inglês; citações no idioma original.
- Manter cruzamentos entre países e interpretações sob demanda.
- Não adicionar cadeias de chamadas de IA nem busca semântica adicional nesta etapa sem necessidade demonstrada.

Validação futura: apenas testes básicos simulados e compilação; buscas reais, qualidade e desempenho ficam com o usuário. Ganho de velocidade ainda não medido.

---

# Histórico das melhorias anteriores

# Melhorias implementadas

Os quatro itens foram implementados. Validação: cinco testes simulados passaram; TypeScript e build Vite concluídos. Nenhuma busca, inferência Qwen ou comparação real de desempenho foi executada.

1. Configurações: Verificar este computador identifica CPU, RAM, GPUs registradas, versão do Ollama e memória de GPU reportada por modelos carregados. Perfil automático é recalculado nesta máquina ao iniciar o Ollama; opção CPU e margem de memória disponíveis. Salvar e aplicar perfil reinicia somente o Ollama gerenciado por esta instalação, se não houver análise/classificação em andamento. Ollama externo exige reinício manual. Margem de memória é verificada antes da geração, não é limite rígido durante a execução.
2. Resumos: entrada reduzida, esquema JSON não repetido nas instruções do Ollama, contexto proporcional à entrada e teto de saída, cache por revisão/texto/modelo/instruções/idioma entre consultas. Novo resumo ignora cache. Etapas e tempo decorrido visíveis; métricas de carga/leitura/geração são registradas. Nenhum ganho de tempo foi medido nesta implementação.
3. Idioma: fontes BR em português, demais fontes em inglês; citações preservadas no original. Versões antigas permanecem no acervo; nova geração aplica a política nova.
4. Resumo ilustrado: botão abre texto e imagens agrupadas pelas referências. Uma imagem editorial por matéria, legenda/crédito quando disponíveis. Imagens são obtidas do HTML/metadados nas novas coletas e baixadas ao abrir a leitura, com cache local e inclusão no backup. Falha de imagem preserva o texto. Sem navegador automatizado nem interpretação visual por IA.

Para ativar: reinicie o Observatório com Encerrar.cmd e Iniciar.cmd, recarregue a página. Em Configurações, Verificar este computador → Usar recomendação → Salvar e aplicar perfil habilita o perfil no Ollama gerenciado. Esse botão não gera resumos.

Resultados visuais, qualidade e desempenho reais serão avaliados pelo usuário. Imagens ausentes nas revisões antigas precisam de nova coleta; páginas com imagem apenas via JavaScript não são cobertas pelo piloto.
