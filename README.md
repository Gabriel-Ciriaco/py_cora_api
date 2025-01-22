# py_cora_api

## Instruções
- Obtenha suas credenciais conforme explicitado em: https://developers.cora.com.br/docs/instrucoes-iniciais

- Você deverá ter:
  - Client_id: `int-hash`
  - Certificado: `certificate.pem`
  - Chave Privada: `private-key.key`

---

### Crie um arquivo `.env`
  Este arquivo será responsável por armazenar em variáveis de ambiente os dados necessários da nossa API.

  Escreva o seguinte nele:
  ```
  CORA_CLIENT_ID=seu_client_id
  ```

---

### Crie a pasta `certificates`
Nessa passta estarão armazenados os arquivos necessários para a comunicação HTTPS da API:
```
project
|   .env
|   api.py
|
|___certificates
    |   certificate.pem
    |   private-key.key
```

---

### Baixando as bibliotecas necessárias
Rode o seguinte código no seu ambiente de execução:
```
pip install -r requirements.txt
```

OBSERVAÇÃO: Recomenda-se rodar o projeto num ambiente virtual (`.venv`)!