# Sistema de Preenchimento Automático de Documentação Técnica

## 🎯 Objetivo

Automatizar a inserção de aprovadores em documentos de configuração (CF) da linha E2, preservando integralmente a estrutura original do arquivo, incluindo fórmulas, estilos e metadados. O sistema altera exclusivamente as células de aprovação após validação do usuário.

---

## 💻 Requisitos de Software

### Ambiente
- **Python**: 3.10 ou superior

### Bibliotecas Necessárias

| Biblioteca | Finalidade |
|------------|-----------|
| `openpyxl` | Manipulação de Excel (preserva estilos e macros) |
| `streamlit` | Interface web e gerenciamento de estado |
| `pymongo` | Integração com MongoDB (NoSQL) |
| `io.BytesIO` | Processamento de arquivos em memória |

### Instalação

```bash
pip install openpyxl streamlit pymongo
```

---

## ⚙️ Lógica de Processamento (Back-end)

### 3.1. Identificação Robusta (Busca Dinâmica)

O sistema utiliza **busca inteligente** ao invés de coordenadas fixas para evitar quebras por mudanças no template.

#### Processo de Identificação

1. **Iteração Controlada**
   - O script deve percorrer as primeiras 30 linhas e 10 colunas da aba `Cover`

2. **Match de Label**
   - Procura pelos textos exatos:
     - `"DOCUMENT TITLE:"`
     - `"AIRCRAFT MODEL:"`

3. **Captura de Valor**
   - Uma vez localizado o rótulo, o valor deve ser extraído da célula imediatamente à direita (offset horizontal +1).

4. **Normalização**
  - Aplicar .strip().upper() nos valores capturados para facilitar a comparação com o banco de dados.

### 3.2. Consulta e Mapeamento

#### Query MongoDB

```python
query = {
    "doc_type": "CF",
    "aircraft": "E2"
}
result = db.approvals_matrix.find_one(query)
```
#### Destino das Informações

**Aba**: `Approvals`  
**Linha**: 5 (ou linha correspondente ao nó ativo)

| Campo | Coluna | Responsável |
|-------|--------|-------------|
| Prepared | F | Preparado por |
| Checked | G | Verificado por |
| Approved | H | Aprovado por |
| Industrialization | I | Industrialização |
| Mat. Process | J | Processo de Material |

### 3.3. Integridade do Arquivo

#### Preservação Completa

```python
workbook = load_workbook(file, keep_vba=True)
```

#### Escrita Localizada
- ✅ **Alterado**: Apenas células de nomes na aba `Approvals`
- ✅ **Preservado**: Todas as outras abas (Ex: AAA, AAB) e informações da `Cover`
- ✅ **Mantido**: Fórmulas, estilos, macros e metadados

---

## 🖥️ Fluxo da Interface (Front-end)

### 1. Área de Upload
- Interface drag-and-drop para arquivos `.xlsx`
- Validação de formato

### 2. Dashboard de Diagnóstico

```
📄 Documento identificado: [CONFIGURATION DOCUMENT - CF]
✈️ Modelo identificado: [E2]
```

### 3. Painel de Validação (Preview)

- **5 campos de texto** pré-preenchidos (`st.text_input`)
- Dados carregados automaticamente do banco
- **Editável**: Permite substituições de última hora

| Campo | Função |
|-------|--------|
| Campo 1 | Prepared By |
| Campo 2 | Checked By |
| Campo 3 | Approved By |
| Campo 4 | Industrialization |
| Campo 5 | Materials Process |

### 4. Botão de Processamento

```
🚀 Gerar Documento Final
```

### 5. Área de Download

```
⬇️ Download: NOME_DO_ARQUIVO_PREENCHIDO.xlsx
```

---

## 🗄️ Estrutura do Banco de Dados

### MongoDB - Coleção: `matrix_configs`

```json
{
  "identifier": {
    "title_keyword": "CONFIGURATION DOCUMENT",
    "prefix": "CF",
    "aircraft": "E2"
  },
  "approvers": {
    "prepared_by": "Nome A",
    "checked_by": "Nome B",
    "approved_by": "Nome C",
    "industrialization": "Nome D",
    "materials_process": "Nome E"
  }
}
```

### Campos de Identificação

- `title_keyword`: Palavra-chave do título do documento
- `prefix`: Prefixo do tipo de documento (CF, etc.)
- `aircraft`: Modelo da aeronave (E2, etc.)

---

## 🛡️ Tratamento de Exceções

### Cenários e Respostas

| Situação | Mensagem/Ação |
|----------|---------------|
| **Rótulo não encontrado** | "❌ Erro de Estrutura: Rótulos de identificação não localizados na aba Cover." |
| **Falta de Match no Banco** | Sistema abre campos de texto vazios para preenchimento manual (primeira configuração) |
| **Arquivo Corrompido/Protegido** | Verificação de proteção por senha antes da abertura |

### Validações Implementadas

1. ✅ Verificação de estrutura da aba `Cover`
2. ✅ Validação de existência de rótulos obrigatórios
3. ✅ Checagem de proteção por senha
4. ✅ Fallback para entrada manual

---

## 📊 Fluxograma do Sistema

```
Upload do Arquivo (.xlsx)
         ↓
Busca Dinâmica de Rótulos (Cover)
         ↓
Extração de Valores (Título + Modelo)
         ↓
Consulta MongoDB (doc_type + aircraft)
         ↓
Preview de Aprovadores (Editável)
         ↓
Validação do Usuário
         ↓
Escrita Localizada (Aba Approvals)
         ↓
Geração em Memória (BytesIO)
         ↓
Download do Arquivo Final
```

---

## 🚀 Exemplo de Uso

### 1. Exemplo de Lógica: Busca por Rótulo (Label) e Preservação de Arquivo
```python
import openpyxl
from copy import copy

def processar_documento_safran(caminho_input, nomes_aprovadores):
    # 1. Carrega o arquivo original mantendo TUDO (estilos, fórmulas, imagens)
    wb = openpyxl.load_workbook(caminho_input, data_only=False)
    ws_cover = wb['Cover']
    ws_approvals = wb['Approvals']

    # 2. BUSCA DINÂMICA: Localiza onde está o "Document Title" e o "Aircraft Model"
    metadata = {}
    labels_para_buscar = {
        "DOCUMENT TITLE:": "title",
        "AIRCRAFT MODEL:": "model"
    }

    # Percorre as primeiras 30 linhas e 10 colunas em busca dos rótulos
    for row in ws_cover.iter_rows(min_row=1, max_row=30, min_col=1, max_col=10):
        for cell in row:
            if cell.value and str(cell.value).strip().upper() in labels_para_buscar:
                label_encontrado = str(cell.value).strip().upper()
                # O valor está na célula à direita (offset: col + 1)
                valor = ws_cover.cell(row=cell.row, column=cell.column + 1).value
                metadata[labels_para_buscar[label_encontrado]] = valor

    print(f"Dados Identificados: {metadata}")

    # 3. VALIDAÇÃO DE SEGURANÇA
    if "CF" in metadata.get('title', '') and metadata.get('model') == "E2":
        print("Documento Validado. Iniciando preenchimento da aba Approvals...")
        
        # 4. PREENCHIMENTO (Exemplo: Linha 5, Colunas F até J)
        # Aqui o programador usaria os nomes vindos do MongoDB ou da edição do usuário
        mapeamento_colunas = {
            6: nomes_aprovadores['prepared'],      # Coluna F
            7: nomes_aprovadores['checked'],       # Coluna G
            8: nomes_aprovadores['approved'],      # Coluna H
            9: nomes_aprovadores['industrial'],    # Coluna I
            10: nomes_aprovadores['mat_process']   # Coluna J
        }

        for col, nome in mapeamento_colunas.items():
            ws_approvals.cell(row=5, column=col).value = nome

        # 5. SALVAMENTO SEGURO (Gera uma cópia, nunca sobrescreve o original sem permissão)
        nome_saida = caminho_input.replace(".xlsx", "_PREENCHIDO.xlsx")
        wb.save(nome_saida)
        return f"Sucesso! Arquivo salvo como: {nome_saida}"
    
    else:
        return "Erro: Documento não corresponde aos critérios (CF + E2)."

# Dados de teste (Simulando o que viria do banco de dados/usuário)
aprovadores_teste = {
    'prepared': 'Fernando',
    'checked': 'Maria',
    'approved': 'Alan',
    'industrial': 'Karla',
    'mat_process': 'Marcos'
}
```
---


## 📄 Licença

Este sistema é destinado ao uso interno para processos de documentação técnica aeronáutica.

---

## 📧 Suporte

Para questões técnicas ou sugestões de melhorias, entre em contato com a equipe de desenvolvimento.
