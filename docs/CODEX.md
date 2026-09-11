# Codex com conta ChatGPT (piloto)

O provedor Codex é uma terceira opção, além de Ollama e OpenAI API. Requer o aplicativo Codex ou seu CLI instalado. Usa login próprio do Observatório, sem copiar a sessão do aplicativo Codex.

1. Reinicie o Observatório e abra Configurações.
2. Escolha **Codex · entrar com ChatGPT (teste)** e clique em **Entrar com ChatGPT**.
3. Abra o link apresentado e conclua o login no navegador.
4. Clique em **Verificar conexão e modelos**, escolha o modelo disponível na sua conta, habilite as análises e salve.

Os documentos selecionados são enviados à OpenAI. As gerações usam os limites do Codex da sua conta; não são ilimitadas nem créditos de API. Não existe fallback automático para a API paga. Ollama e OpenAI API continuam disponíveis.

O painel apresenta o percentual usado, restante e renovação de cada janela informada pelo Codex, com aviso a partir de 90% de uso. Essa cota é compartilhada com os outros usos de Codex da conta. Os tokens registrados pelo Observatório são contados separadamente, somente para gerações registradas neste acervo; valores ausentes aparecem como contagem parcial. A atualização ocorre a cada minuto, podendo aguardar uma geração em andamento.

O limite de resposta configurado para API/Ollama não é um teto rígido de tokens do Codex. O provedor pede respostas curtas e usa esforço baixo quando o modelo oferece essa opção. O processamento aceita apenas respostas textuais e rejeita pedidos de ferramentas ou permissões.

O login é armazenado em `runtime/observatorio-codex`, fora do pacote de distribuição. Não compartilhe essa pasta. A integração recebeu testes simulados e compilação da interface; o login e a geração real devem ser validados pelo usuário.

Referência: https://learn.chatgpt.com/docs/app-server
