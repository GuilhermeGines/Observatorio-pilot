# Gemini e múltiplas configurações de IA

Em Configurações, selecione Gemini. Abra o Google AI Studio pelo botão, entre com sua conta Google e crie uma chave da API. Guarde a chave no Observatório, verifique a conexão e os modelos, escolha o modelo, habilite as análises e clique em **Salvar esta IA**. A verificação lista modelos sem gerar conteúdo.

O botão abre o AI Studio; não é um login OAuth integrado. OAuth exigiria um projeto Google Cloud e credenciais próprias de aplicativo. A integração usa a API oficial compatível com OpenAI e envia os textos ao Google, não à OpenAI. A biblioteca cliente é compartilhada, mas o endereço e a chave são exclusivos do Gemini.

A cota gratuita depende do projeto e do modelo. Não é possível deduzir gratuidade da listagem de modelos. Confira o nível de faturamento no AI Studio: um projeto pago pode gerar cobranças. No nível gratuito, o Google pode usar os textos para melhorar os produtos. O aplicativo não ativa faturamento, não compra créditos e não troca de serviço automaticamente.

## Vários modelos

Salvar outro provedor ou modelo mantém as configurações anteriores. Salvar o mesmo provedor e modelo atualiza sua configuração. As chaves são compartilhadas entre os modelos de um mesmo provedor e guardadas no cofre do sistema; não fazem parte do banco nem do Git. Os perfis podem ser editados ou removidos em **IAs salvas**.

Com mais de um modelo habilitado, use a seta **Modelos** junto ao botão do resumo e marque quais devem participar. Sem marcação, usa a última configuração disponível. Confira a lista de destinatários antes de gerar. Cada modelo recebe os documentos de seu próprio plano, gera um resumo separado e consome sua própria cota. A execução é sequencial; falha de um modelo não apaga os resumos já salvos nem aciona repetição automática.

Use **Resumo exibido** para alternar entre resultados. Cruzamentos usam o modelo do resumo selecionado e ficam associados àquela versão.

## Indicadores de uso

Os cartões compactos atualizam a cada minuto e após as gerações. Codex mostra os percentuais e renovações fornecidos pelo serviço, compartilhados com os demais usos da conta. Gemini e OpenAI API mostram tokens registrados no Observatório, com aviso de contagem parcial se necessário; não se atribui um percentual a uma cota desconhecida. Consulte o AI Studio para o limite real do projeto Gemini. Ollama mostra uso local, sem cota de API. Tokens registrados incluem chamadas cuja resposta foi rejeitada quando o serviço devolveu uso; falhas sem informação de uso não podem ser contabilizadas.

Validação da implementação: testes simulados de seleção de perfis, resposta Gemini, referências e uso; sem chamadas reais aos modelos. A conexão real depende da chave do usuário.

Referências oficiais:
- https://ai.google.dev/gemini-api/docs/openai
- https://ai.google.dev/gemini-api/docs/api-key
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://ai.google.dev/gemini-api/docs/pricing
