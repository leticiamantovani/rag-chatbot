# Things to solve

- verify classes
- verify instances
-verify best way to use the dependenc es
-verify to use the classic ollama function
- verify try catch
- verify best way to return things in the response
- integrate s3
- where the best way to put prompt on the prompt?
- chat api doesnt have to put collection name - it should retrieve automatically
- as apis estao lentas
- testes unitarios - usa?
- retorno da api

embeddings = create_embeddings() e model = create_model() em module level (chat_service.py:9-10) — anti-pattern. Roda no import, dificulta teste, dificulta swap. Idealmente injetar via Depends. Vale uma refatoração separada.
Histórico crescendo sem bound — em conversas longas, list_by_conversation carrega tudo e injeta no prompt. Em produção: paginação ou janela deslizante (últimas N mensagens) ou summarização.
Prompt template — hoje é f-string inline no service. Em produção, costuma ser um arquivo separado / langchain.PromptTemplate.

- logging e exceptions