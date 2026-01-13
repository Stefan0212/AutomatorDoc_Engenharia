# AutomatorDoc: Automação de Fluxo de Aprovação (Engenharia)

## 📌 Visão Geral
O **AutomatorDoc** é uma solução de automação em Python projetada para eliminar o esforço manual de preenchimento de documentos de engenharia (foco inicial em Configuration Documents - CF). O sistema identifica automaticamente o contexto do documento e sugere os aprovadores responsáveis com base em uma matriz de competência armazenada em banco de dados.

## 🎯 Objetivo
Reduzir o tempo de processamento burocrático de documentos técnicos da linha E2, garantindo 100% de precisão nos nomes dos aprovadores e mantendo a integridade visual dos arquivos Excel (Templates Safran).

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.10+
- **Frontend:** Streamlit (Interface Web)
- **Manipulação de Planilhas:** Openpyxl (Escrita mantendo formatação original)
- **Banco de Dados:** MongoDB (Armazenamento flexível da matriz de aprovadores)

## 🔄 Fluxo de Valor
1. **Upload:** O usuário insere o arquivo `.xlsx` (Ex: CF-H211290).
2. **Análise:** O sistema lê a aba `Cover` para identificar o "Document Title" e o "Aircraft Model".
3. **Sugestão:** O sistema busca no MongoDB os nomes para as etapas de *Prepared, Checked, Approved, Industrialization e Mat. Process*.
4. **Validação Humana:** O usuário revisa os nomes na interface e pode editá-los se houver substituições pontuais.
5. **Geração Segura:** O sistema realiza a "injeção" dos nomes validados na aba `Approvals` do arquivo original. O resultado é o seu documento completo, preservando todas as abas técnicas (AAA, AAB, AAC, etc.), formatações e logotipos originais, sem perda de metadados.
