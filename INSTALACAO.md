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
EXCEL_PASSWORD=
```

**Notas:**
- **MONGODB_URI:** 
  - Para MongoDB local: `mongodb://localhost:27017/`
  - Para MongoDB Atlas: `mongodb+srv://usuario:senha@cluster.mongodb.net/` (substitua `usuario` e `senha` pelas suas credenciais)
- **EXCEL_PASSWORD:** Deixe vazio (variável não utilizada atualmente, reservada para futuras implementações)

### 3. Popular o banco de dados

Execute o script de seed para popular o MongoDB com dados iniciais:

```bash
python db_seed.py
```

### 4. Executar a aplicação

```bash
python -m streamlit run app.py
```

**Nota:** Se o comando `streamlit` não for reconhecido no Windows, use `python -m streamlit run app.py` ao invés de apenas `streamlit run app.py`.

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
- Confirme se os rótulos "DOCUMENT TITLE:" e "AIRCRAFT MODEL:" estão presentes na aba Cover
- Os valores devem estar nas células à direita dos rótulos
- Certifique-se de que o arquivo não está protegido por senha (ou configure `EXCEL_PASSWORD` no `.env`)
