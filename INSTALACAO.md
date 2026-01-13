# Guia de Instalação - AutomatorDoc

## Pré-requisitos

- Python 3.10 ou superior
- MongoDB instalado e rodando (local ou remoto)

## Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=technical_docs
EXCEL_PASSWORD=sua_senha_aqui
```

**Nota:** Ajuste `MONGODB_URI` conforme sua configuração do MongoDB. Se estiver usando MongoDB Atlas, use a string de conexão fornecida.

### 3. Popular o banco de dados

Execute o script de seed para popular o MongoDB com dados iniciais:

```bash
python db_seed.py
```

### 4. Executar a aplicação

```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## Estrutura de Arquivos

```
.
├── app.py                 # Aplicação Streamlit principal
├── excel_handler.py       # Módulo de manipulação Excel
├── db_connection.py       # Módulo de conexão MongoDB
├── db_seed.py            # Script de população do banco
├── requirements.txt       # Dependências Python
├── .env                  # Configurações (não versionado)
└── README.md             # Documentação principal
```

## Troubleshooting

### Erro de conexão com MongoDB

- Verifique se o MongoDB está rodando
- Confirme se a URI no `.env` está correta
- Teste a conexão manualmente: `mongosh "mongodb://localhost:27017/"`

### Erro ao processar Excel

- Verifique se o arquivo tem as abas "Cover" e "Approvals"
- Confirme se as células E15 e E23 estão preenchidas na aba Cover
- Certifique-se de que o arquivo não está protegido por senha (ou configure `EXCEL_PASSWORD` no `.env`)
