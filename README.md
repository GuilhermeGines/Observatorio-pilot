# Observatório · piloto local

Gemini e múltiplas IAs: salve modelos independentes, selecione quais geram o resumo e acompanhe o uso em cartões compactos. Consulte [docs/GEMINI-E-MODELOS.md](docs/GEMINI-E-MODELOS.md) para conexão, cotas e limites.

Provedor experimental Codex com login ChatGPT, seleção dos modelos disponíveis na conta e painel de limites e tokens. Ollama e OpenAI API permanecem disponíveis. Ativação: [docs/CODEX.md](docs/CODEX.md).

Atualização 11/09/2026: imagens removidas. A síntese por país seleciona trechos relevantes, agrupa repetições e usa referências numeradas. Consulte docs/FILA.md para o estado atual; referências a imagens em registros anteriores descrevem uma funcionalidade descontinuada.

Melhorias atuais: verificador do computador e perfil automático em Configurações; resumos com cache entre consultas, Brasil em português e demais fontes em inglês. Detalhes de ativação e limites em docs/FILA.md.

Catálogo ampliado: 170 fontes únicas; por país, cinco por tema, dez veículos, um governo principal e cinco universidades. A busca seleciona fontes pelo assunto antes da coleta. Expressões desconhecidas usam classificação curta local; na dúvida, selecione um tema. Detalhes e limitações em docs/CATALOGO.md.

Fluxo atual: **Preparar resumo** gera somente uma síntese com referências. Depois, **Preparar cruzamentos** gera comparações e interpretações sob demanda. Cada etapa é salva separadamente. A geração de áudio e roteiro foi removida.


Explore notícias e documentos de Brasil, Estados Unidos, China e Rússia no navegador. Colete em fontes cadastradas, preserve evidências e compare perspectivas com referências. O programa e o acervo ficam no computador; não há hospedagem pública, Docker ou servidor de banco separado.

## Começar no Windows

1. Abra a pasta do aplicativo e dê dois cliques em **Iniciar.cmd**.
2. O navegador abre em direcionando o IP e a porta. Mantenha a janela de execução aberta. Para encerrar, pressione `Ctrl+C` nela ou abra **Encerrar.cmd**. Este último verifica a identidade do processo antes de encerrá-lo e também funciona quando o piloto está em segundo plano.
3. Escolha os países no globo ou nos botões, uma palavra-chave, temas e as datas de publicação. Use **Buscar no acervo** ou **Buscar nas fontes**.
4. Abra os documentos para ver os trechos lidos, a publicação original, a coleta e as revisões. Consulte **Cobertura** para ver as fontes ausentes.
5. Use **Salvar no histórico** para tornar a consulta visível no histórico. Reabrir reutiliza evidências e análises, sem coletar ou pagar novamente.

Nesta instalação em `C:\ObservatorioFontes`, o ambiente Python e a interface já estão preparados. A distribuição compartilhável inclui a interface compilada: **Node não é necessário para executar**.

### Primeira instalação em outro computador

É necessário **Python 3.11 ou superior** e internet na instalação. Instale pelo [site oficial do Python](https://www.python.org/downloads/) e marque a opção de adicionar Python ao PATH. Depois abra `Iniciar.cmd`: o instalador cria `.venv` e baixa as dependências fixadas em `requirements-lock.txt`. Isso não exige privilégios administrativos se a pasta permitir escrita. Alternativamente, execute `Instalar.ps1` pelo PowerShell.

No macOS/Linux, com Python 3.11+ e suporte a venv: `sh iniciar.sh`. Essas plataformas não foram validadas neste piloto; a instalação foi testada em Windows. O cofre de credenciais depende do sistema.

## O que está implementado

- Três páginas: Explorar, Histórico e Configurações. Interface em português, sem fontes tipográficas ou mapas remotos.
- Globo ortográfico com geometria real de países, rotação por arraste/teclado, zoom e seleção múltipla. BR, US, CN e RU em verde; demais países bloqueados. Botões acessíveis espelham a seleção.
- Dez temas: geopolítica, política nacional, ciência, física, astronomia, tecnologia/IA, economia/comércio, energia/clima/meio ambiente, defesa/segurança e saúde/pesquisa médica.
- Catálogo de **40 veículos jornalísticos (10 por país), oito universidades e 12 instituições públicas/científicas**. RSS/Atom e descoberta limitada de links de páginas. Status real por canal e falha individual por conteúdo.
- Busca literal em título/texto lido, sem distinção de acentos ou maiúsculas. A palavra-chave não altera países. Temas usam vocabulário multilíngue e podem errar.
- Datas de publicação preservadas com origem e fuso editorial; datas de coleta separadas. Intervalo inclusivo, data única e atalho Ontem. Itens sem publicação verificável são excluídos do filtro temporal e contabilizados.
- SQLite local, documentos em JSON legível, revisões por alteração de conteúdo, prevenção de duplicação e preservação de texto já lido quando uma releitura falha. Consultas contêm instantâneos das evidências.
- Com sua API: resumos em PT-BR, afirmações com autor/período/local, cruzamentos limitados a pares candidatos por tema/termos/período, hipóteses separadas de observações, alternativas, evidência contrária, lacunas e falas sobre outro país com atribuição específica.
- Referências da IA validadas: ID deve pertencer à entrada; o trecho deve existir literalmente no texto enviado; país deve coincidir com a fonte. Erros rejeitam a análise e preservam o acervo. Isso não garante que toda interpretação do modelo seja correta.
- Análises versionadas, configuração/modelo/prompt e tokens retornados registrados. Roteiro, áudio em uma voz, player, download e cache local por versão da análise.
- Exportação JSON de consulta e backup ZIP consistente do SQLite, documentos e áudios. Restauração para pasta nova com verificação de integridade.

## Configurar a OpenAI

Não há chave incluída. Sem chave, o aplicativo coleta e consulta evidências reais; **não produz análises fictícias**. Em Configurações:

1. Cadastre sua própria API key. Ela vai para o cofre de credenciais do sistema via `keyring`, nunca para o bundle, SQLite, logs ou Git. Não existe fallback que a grave em texto simples.
2. Informe um modelo da sua conta que aceite **Responses API e saídas estruturadas**. O valor inicial é `gpt-5.4-mini`, configurável; disponibilidade depende da conta. O teste consulta os metadados do modelo, sem enviar documentos, e não certifica saldo ou sucesso de uma futura geração.
3. Ajuste máximo de documentos, caracteres por documento e tokens de saída. Habilite o envio de textos. Cada análise mostra antes o tamanho da entrada e pede acionamento explícito.
4. Para ouvir, acione a geração de áudio. Usa `gpt-4o-mini-tts`, voz `coral`, com instrução de português brasileiro. É voz gerada por IA, não gravação humana. A chamada é adicional; depois o MP3 fica reutilizável.

**API e assinatura do ChatGPT têm cobranças separadas.** Limites de tamanho não são promessa de orçamento monetário. Tokens reais retornados ficam registrados; preços, saldo e cobrança final devem ser consultados na conta OpenAI. Chamadas sem resposta ou rejeitadas por validação podem ter sido cobradas. Não há repetição automática de chamadas pagas.

`OPENAI_API_KEY` no ambiente do processo é uma alternativa ao cofre e tem precedência. O programa não lê `.env` automaticamente; `.env.example` é somente referência. Chaves de ambiente precisam ser removidas no ambiente antes de reiniciar.

Implementação consultada na documentação oficial: [saídas estruturadas](https://developers.openai.com/api/docs/guides/structured-outputs), [texto para fala](https://developers.openai.com/api/docs/guides/text-to-speech). As chamadas usam `store=False` para análises, sem ferramentas de navegação do modelo. Textos externos são tratados como dados, não instruções.

## Cobertura e limites honestos

Veja **[docs/CATALOGO.md](docs/CATALOGO.md)** e **[docs/source-audit.json](docs/source-audit.json)** para seleção, canais e testes reais. O status da instalação em Configurações se atualiza a cada coleta. Uma URL cadastrada não significa fonte plenamente integrada.

- A coleta percorre **até 60 itens de feed ou 30 links de página**, e lê até o número configurado de artigos por fonte (padrão: 3; máximo: 10). Isso é uma amostra recente, não todo o site. Itens fora do limite ficam como metadados/trechos, se distribuídos pela fonte.
- Links de página podem apontar a comunicados ou conteúdo institucional sem data. Itens sem data não entram na análise por período. Datas antigas, como **23/09/2018**, dependem do acervo ou de uma URL histórica aberta que você importe em Configurações. Ausência de resultados não prova inexistência.
- Somente sites/domínios cadastrados são lidos. Há verificação de robots.txt, redirecionamentos e endereços públicos. Bloqueio, 403, timeout, autenticação e paywall são relatados, sem contorno de restrições. Não há sessão de assinante implementada no piloto.
- Extração automática pode omitir tabelas, imagens e elementos de páginas. PDFs abertos podem ser importados por URL; até 80 páginas são extraídas, sem OCR. Sem data editorial verificável ficam excluídos das consultas por data.
- Trecho de feed, texto extraído, metadados e conteúdo restrito são diferenciados. A IA só recebe o que foi efetivamente lido, limitado ao tamanho configurado.
- Notícias institucionais identificam links a DOI, preprints, artigos e dados quando presentes. **O estudo vinculado não é automaticamente baixado nem sua revisão por pares confirmada**. Plataformas de preprints são sinalizadas; os demais vínculos ficam com revisão não verificada.
- Apuração própria não é presumida. Entrevista/investigação/opinião/reprodução são sinalizadas somente por indícios explícitos. Ausência de indício fica “apuração não verificada”. Grupos por crédito e semelhança são preventivos, não prova de independência ou de cópia.
- Uma fonte oficial comprova que uma instituição fez uma declaração; não torna o conteúdo automaticamente verdadeiro. Relações textuais não são correlação estatística nem causalidade. Comparações e atribuições precisam de revisão humana.
- O acervo pode crescer. Não há indexação semântica/vetorial neste piloto. As consultas exibem até 200 resultados; reduza filtros para ver outros recortes.

## Dados, backup, restauração e atualizações

Por padrão os dados ficam em `data/`: `observatorio.sqlite3`, `documents/`, `audio/`, `backups/`. Essa pasta é ignorada pelo Git. Para mudar, defina `OBS_DATA_DIR` como caminho absoluto antes de iniciar. O programa cria as pastas automaticamente. O backup contém informações do seu acervo e deve ser compartilhado apenas se você quiser compartilhar esses dados. Chaves não são incluídas.

Em Configurações, clique **Criar backup completo** e **Baixar backup**. Para restaurar, encerre o aplicativo e execute na pasta do programa:

```powershell
.\.venv\Scripts\python.exe tools\restore_backup.py "C:\caminho\observatorio-backup.zip" "C:\ObservatorioFontes\data-restaurada"
$env:OBS_DATA_DIR = 'C:\ObservatorioFontes\data-restaurada'
.\.venv\Scripts\python.exe launcher.py
```

O destino deve ser novo/vazio. O restaurador recusa sobrescrita e caminhos externos ao destino. Guarde o backup original até conferir o resultado. Para usar o novo destino nas próximas sessões, mantenha a variável de ambiente configurada. Cadastre a chave novamente no novo perfil de dados.

Para atualizar o código, encerre o aplicativo, faça um backup e substitua somente arquivos do programa, **preservando `data/` e `.venv/`**. Execute o instalador para atualizar dependências. O SQLite inicia/mantém o esquema automaticamente. Uma coleta interrompida é sinalizada no reinício, sem apagar documentos já persistidos.

## Compartilhar o código

O repositório local está preparado. Não foi criado repositório remoto nem publicada informação. Compartilhe o ZIP de distribuição ou escolha seu próprio repositório GitHub. Inclua `app/static/`, pois contém a interface compilada. Não inclua `data/`, `.venv/`, `node_modules/`, chaves, backups, áudios ou logs pessoais. `.gitignore` cobre esses arquivos.

O código do piloto é disponibilizado sob MIT (LICENSE). Conteúdo coletado pertence aos respectivos titulares e não é licenciado pelo projeto. Dados geográficos: `world-atlas`/Natural Earth; veja THIRD_PARTY.md.

## Desenvolvimento e testes

Python 3.11+; Node 18+ apenas para desenvolver/compilar a interface. No Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
cd frontend
npm ci
npm test
npm run build
```

Para desenvolvimento com recarga: defina `OBS_DEV=1`, execute `uvicorn app.main:app --host 127.0.0.1 --port 8765` e, em outra janela na pasta frontend, `npm run dev`. O Vite encaminha `/api` ao serviço local. A distribuição normal serve frontend e API juntos.

Testes de IA, áudio e alguns cenários de erro usam **fixtures explicitamente sintéticas em pastas temporárias**. Nada sintético é injetado no acervo real. Sem chave fornecida, a análise e a voz não foram testadas com chamadas reais pagas. Veja [docs/VALIDACAO.md](docs/VALIDACAO.md) para resultados e limites da entrega.

O serviço escuta **somente em 127.0.0.1**. Não altere para `0.0.0.0` nem use túnel público: o piloto é pessoal, sem sistema multiusuário. Há validação de Host, Origin e token de sessão para alterações, sem CORS aberto.
