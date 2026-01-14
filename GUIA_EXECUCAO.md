# 🚀 Guia de Execução - AutomatorDoc

## Próximos Passos para Rodar o Sistema

### 1️⃣ Verificar Pré-requisitos

#### Python 3.10+
```bash
python --version
```
Se não tiver Python instalado, baixe em: https://www.python.org/downloads/

#### MongoDB
- **Opção A - MongoDB Local:**
  - Baixe e instale: https://www.mongodb.com/try/download/community
  - Inicie o serviço MongoDB
  
- **Opção B - MongoDB Atlas (Cloud):**
  - Crie uma conta gratuita: https://www.mongodb.com/cloud/atlas
  - Crie um cluster e obtenha a string de conexão

### 2️⃣ Instalar Dependências

Abra o terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

Isso instalará:
- `streamlit` - Interface web
- `openpyxl` - Manipulação de Excel
- `pymongo` - Conexão MongoDB
- `python-dotenv` - Gerenciamento de variáveis de ambiente

### 3️⃣ Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

**Windows (PowerShell):**
```powershell
New-Item -Path .env -ItemType File
```

**Linux/Mac:**
```bash
touch .env
```

Adicione o seguinte conteúdo no arquivo `.env`:

```env
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=technical_docs
EXCEL_PASSWORD=
```

**Para MongoDB Atlas (cloud), use:**
```env
MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
DB_NAME=technical_docs
EXCEL_PASSWORD=
```

**Importante:**
- **MONGODB_URI:** A senha do MongoDB vai dentro desta variável quando você usa Atlas (formato: `mongodb+srv://usuario:senha@cluster...`)
- **EXCEL_PASSWORD:** Deixe sempre vazio (não é usado atualmente no código)

### 4️⃣ Popular o Banco de Dados

Execute o script de seed para criar a estrutura inicial:

```bash
python db_seed.py
```

Você deve ver mensagens como:
```
✓ Inserido: CONFIGURATION DOCUMENT - E2
✓ Inserido: CONFIGURATION DOCUMENT - E175
✓ População do banco de dados concluída!
```

### 5️⃣ Executar a Aplicação

Inicie o servidor Streamlit:

**Opção 1 (recomendado - funciona sempre):**
```bash
python -m streamlit run app.py
```

**Opção 2 (se o comando streamlit estiver no PATH):**
```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em:
**http://localhost:8501**

Se não abrir automaticamente, copie e cole a URL no navegador.

### 6️⃣ Usar o Sistema

1. **Upload do Arquivo:**
   - Clique em "Selecione o arquivo Excel (.xlsx)"
   - Escolha um arquivo que tenha:
     - Aba `Cover` com os rótulos `DOCUMENT TITLE:` e `AIRCRAFT MODEL:`
     - Aba `Approvals` para preenchimento

2. **Validação:**
   - O sistema identificará automaticamente o documento e modelo
   - Os aprovadores serão carregados do banco de dados
   - Revise e edite os campos se necessário

3. **Geração:**
   - Clique em "🚀 Gerar Documento Final"
   - Baixe o arquivo processado com sufixo `_PREENCHIDO.xlsx`

---

## 🔧 Troubleshooting

### Erro: "Erro ao conectar ao MongoDB"
- ✅ Verifique se o MongoDB está rodando (local) ou se a URI está correta (Atlas)
- ✅ Teste a conexão: `mongosh "mongodb://localhost:27017/"` (local) ou use o MongoDB Compass

### Erro: "Rótulos de identificação não localizados"
- ✅ Verifique se a aba `Cover` contém os rótulos exatos: `DOCUMENT TITLE:` e `AIRCRAFT MODEL:`
- ✅ Os valores devem estar nas células à direita dos rótulos

### Erro: "Nenhum registro encontrado no banco de dados"
- ✅ Execute `python db_seed.py` novamente
- ✅ Verifique se a coleção `matrix_configs` foi criada no MongoDB

### Erro ao instalar dependências
- ✅ Use `pip install --upgrade pip` antes de instalar
- ✅ No Windows, pode ser necessário usar `python -m pip install -r requirements.txt`

### Porta 8501 já está em uso
- ✅ Feche outras instâncias do Streamlit
- ✅ Ou use: `python -m streamlit run app.py --server.port 8502`

---

## 📋 Checklist de Execução

- [ ] Python 3.10+ instalado
- [ ] MongoDB instalado/Atlas configurado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Arquivo `.env` criado e configurado
- [ ] Banco de dados populado (`python db_seed.py`)
- [ ] Aplicação rodando (`python -m streamlit run app.py`)
- [ ] Arquivo Excel de teste pronto para upload

---

## 🎯 Próximas Melhorias (Opcional)

Após o sistema estar funcionando, você pode considerar:

1. **Adicionar mais configurações ao banco:**
   - Edite `db_seed.py` para incluir outros tipos de documentos
   - Adicione mais modelos de aeronave

2. **Personalizar interface:**
   - Ajuste cores e layout em `app.py`
   - Adicione logos ou branding

3. **Autenticação:**
   - Implemente login de usuários
   - Controle de acesso por perfil

---

**Pronto! Seu sistema está configurado e funcionando! 🎉**
