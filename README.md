# Observatório

Pesquise notícias e documentos de Brasil, Estados Unidos, China e Rússia. Gere resumos narrativos por país e compare perspectivas com referências verificáveis, mantendo o acervo no seu computador.

## Instalação

1. Instale [Python 3.11 ou superior](https://www.python.org/downloads/) e marque **Add Python to PATH**.
2. Baixe este repositório em **Code → Download ZIP** e extraia a pasta, ou clone pelo Git.
3. Abra **Iniciar.cmd**. As dependências serão instaladas e o navegador abrirá em `http://127.0.0.1:8765`.
4. Em **Configurações**, conecte a IA e escolha o modelo.

Não precisa instalar Node para usar. No macOS/Linux, execute `sh iniciar.sh` (plataformas ainda não validadas).

## Como usar

- Escolha países, palavra-chave e período: **Hoje**, **Ontem**, **Semana** ou datas personalizadas. O tema pode ser identificado automaticamente.
- Busque nas fontes ou no acervo. A **busca ampliada com Gemini + GDELT** pode ser habilitada nas Configurações.
- Gere o **resumo por país** e, quando quiser, os **cruzamentos**. As novas análises são em português BR; as citações preservam o idioma original.
- Salve a pesquisa no histórico para consultar novamente.

**IAs disponíveis:** Gemini, OpenAI API, Codex com conta ChatGPT e Ollama local. Cada serviço utiliza seus próprios limites; a identificação automática do tema e a busca ampliada também podem consumir IA.

Os resultados dependem das fontes acessíveis e das datas verificáveis. Ausência de resultados não significa ausência de notícias.

## Dados e documentação

Seu acervo fica em `data/`, fora do Git. Faça backup em Configurações antes de atualizar e preserve essa pasta. Chaves ficam no cofre do sistema ou no ambiente, fora do repositório.

Detalhes: [Gemini e modelos](docs/GEMINI-E-MODELOS.md) · [Codex](docs/CODEX.md) · [Catálogo de fontes](docs/CATALOGO.md) · [Validação](docs/VALIDACAO.md).

Licença [MIT](LICENSE). Conteúdos coletados pertencem aos respectivos titulares.

## Releases

### 12/09/2026 — Pesquisa e resumos (`24cfcf7`)

- Busca ampliada com Gemini + GDELT nas Configurações e seleção dinâmica de fontes por assunto.
- Filtro **Semana**, resumos em abas por país e carregamento no próprio bloco.
- Referências recolhidas para uma leitura mais limpa e indicadores de cota Gemini.
- Novas análises em português BR, preservando citações originais.

### Integração Gemini (`17c4fdd`)

- Gemini e múltiplos perfis de IA, seleção de modelos e indicadores de uso.
