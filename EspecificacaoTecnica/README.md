# Sistema de Preenchimento Automático de Documentação Técnica

## 📋 Visão Geral

Sistema desenvolvido para automatizar o preenchimento de documentação técnica aeronáutica, seguindo o padrão MVC simplificado com interface web, processamento inteligente de planilhas Excel e armazenamento em banco de dados NoSQL.

### Arquitetura

- **View (Interface)**: Streamlit (Web UI)
- **Controller (Lógica)**: Python com openpyxl
- **Model (Dados)**: MongoDB

---

## 🔧 Requisitos Técnicos

### Ambiente
- **Python**: 3.10 ou superior

### Dependências Principais

```bash
streamlit          # Interface do usuário e gerenciamento de estado
openpyxl          # Leitura e escrita em arquivos .xlsx mantendo estilos e imagens
pymongo           # Driver de conexão com o banco de dados
python-dotenv     # Gerenciamento de credenciais e chaves de API
```

### Instalação

```bash
pip install streamlit openpyxl pymongo python-dotenv
```

---

## 🗄️ Estrutura do Banco de Dados

### MongoDB - Coleção: `approvals_matrix`

**Schema do Documento:**

```json
{
  "_id": "ObjectId",
  "unit_key": "CONFIGURATION DOCUMENT",
  "aircraft_model": "E2",
  "approvers": {
    "prepared_by": "Bruno Serpa",
    "checked_by": "M. Camargo",
    "approved_by": "Alan Araujo",
    "industrialization": "Karla Castro",
    "mat_process": "James Delpinto"
  }
}
```

**Campos de Busca:**
- `documentTitle_key`: Chave primária (coluna C, linha 15 na aba Cover)
- `aircraft_model`: Filtro secundário (coluna E, linha 23)

---

## ⚙️ Fluxo de Execução

### 1. Captura e Leitura
- Upload do arquivo via `st.file_uploader`
- Carregamento com `openpyxl`:
  - `data_only=False`: Preserva fórmulas
  - `data_only=True`: Lê apenas valores calculados
  - `keep_vba=True`: Mantém macros (se aplicável)

```python
workbook = load_workbook(file, keep_vba=True)
```

### 2. Identificação do Contexto
- **Aba**: Cover
- **Células de referência**:
  - `E15`: DOCUMENT TITLE (documentTitle_key)
  - `E23`: AIRCRAFT MODEL (aircraft_model)

### 3. Consulta ao Banco

```python
query = {
    "documentTitle_key": value_from_e15,
    "aircraft_model": value_from_e23
}
data = db.approvals_matrix.find_one(query)
```

### 4. Mapeamento de Células

**Aba 'Approvals' - Mapeamento Dinâmico:**

| Campo | Célula | Descrição |
|-------|--------|-----------|
| `prepared_by` | E5 | Preparado por |
| `checked_by` | F5 | Verificado por |
| `approved_by` | G5 | Aprovado por |
| `industrialization` | H5 | Industrialização |
| `mat_process` | I5 | Processo de Material |

### 5. Escrita e Formatação
- Inserção dos dados nas células mapeadas
- Preservação de formatação (Arial, tamanho 11)
- Uso de `NamedStyle` para manter estilos existentes

### 6. Buffer de Memória e Download
- Arquivo salvo em memória (`BytesIO`)
- Download direto via Streamlit
- **Sem gravação em disco** para evitar problemas de concorrência

---

## 🛡️ Tratamento de Exceções

### Cenários Previstos

| Situação | Ação |
|----------|------|
| **Template Inválido** | Erro controlado se abas Cover ou Approvals não existirem |
| **Dados Ausentes** | Preenchimento manual + opção "Salvar como novo padrão" |
| **Célula Bloqueada** | Verificação de proteção por senha (credencial no `.env`) |

---

## 📂 Estrutura do Projeto

```
project/
├── app.py                 # Aplicação Streamlit principal
├── excel_handler.py       # Módulo de leitura/escrita Excel
├── db_seed.py            # Script de população inicial do MongoDB
├── .env                  # Credenciais e configurações
└── requirements.txt      # Dependências do projeto
```

---

## 🚀 Backlog de Desenvolvimento

### Tarefas Pendentes

- [ ] Criar script `db_seed.py` para popular o MongoDB inicial
- [ ] Desenvolver módulo `excel_handler.py` com funções de leitura/escrita
- [ ] Desenvolver `app.py` (Streamlit) para integração completa
- [ ] Testar persistência de imagens e logotipos após salvamento

---

## 📝 Configuração Inicial

### 1. Variáveis de Ambiente (.env)

```env
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=technical_docs
EXCEL_PASSWORD=sua_senha_aqui
```

### 2. Execução

```bash
streamlit run app.py
```

---

## 🔒 Segurança

- Credenciais gerenciadas via `python-dotenv`
- Processamento em memória (sem arquivos temporários)
- Validação de templates antes do processamento

---

## 📄 Licença

Este projeto é destinado ao uso interno da organização.
