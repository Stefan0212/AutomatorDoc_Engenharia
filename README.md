# Proposta de Projeto: AutomatorDoc - Engenharia Safran

# 1. Visão Geral do Projeto
O AutomatorDoc é uma ferramenta de automação interna desenvolvida para otimizar o preenchimento de documentos de configuração e aprovação em Excel. O sistema atua como uma ponte entre o fluxo de trabalho de engenharia (SCP-DEV-1000) e a documentação final, eliminando o preenchimento manual repetitivo.

# 1.1 O Problema
Atualmente, engenheiros e analistas gastam tempo manual inserindo nomes de aprovadores e dados de cabeçalho em planilhas Excel. Esse processo é:
- Suscetível a erros: Nomes digitados incorretamente podem invalidar auditorias.
- Ineficiente: Profissionais de alto nível realizam tarefas de "copia e cola".
- Descentralizado: Não há um repositório único que relacione "Tipo de Documento" x "Aprovadores Responsáveis".

# 1.2 O Objetivo
Desenvolver um protótipo funcional que automatize o preenchimento da aba Approvals, garantindo que os nomes inseridos estejam sempre de acordo com o tipo de documento que vai ser preenchido. Como também ele faça o preenchimento correto das pessoas que aprovam esse documento.

# 2. Lógica do Programa (Workflow)
O sistema operará em quatro etapas principais:
- Entrada (Input): O usuário faz o upload da planilha modelo (template padrão).
- Identificação: O script lê a célula do Document Title (ex: "CONFIGURATION DOCUMENT") para entender o contexto.
- Consulta (Database): O sistema busca no MongoDB quem são os aprovadores vinculados àquele documento que fizeram upload.
- Processamento e Saída: O Python preenche as células específicas na aba "Approvals" e gera um arquivo pronto para distribuição.

# 3. Arquitetura Técnica

# 3.1 Stack Tecnológica
- Linguagem: Python 3.10+ (Padrão de mercado para automação).
- Interface: Streamlit (Permite criar um dashboard web funcional com poucas linhas de código).
- Manipulação de Excel: openpyxl (Biblioteca que preserva estilos, fórmulas e imagens originais do Excel).
- Banco de Dados: MongoDB (NoSQL). Escolhido pela flexibilidade em armazenar diferentes estruturas de aprovadores por projeto.

# 3.2 Estrutura de Dados (MongoDB)
# Coleção sugerida: matriz_aprovacao
JSON
{
  "document_title": "CONFIGURATION DOCUMENT",
  "aircraft_model": "E2",
  "workflow_step": "Engineering Release",
  "approvers": {
    "prepared_by": "Bruno Serpa",
    "checked_by": "M. Camargo",
    "approved_by": "Alan Araujo",
    "industrialization": "Karla Castro",
    "materials_process": "James Delpinto"
  },
  "last_update": "2025-10-22"
}

# 5. Roadmap de Desenvolvimento (MVP)
Fase 1 (Protótipo): Script Python simples que lê um Excel local e preenche nomes estáticos.
Fase 2 (Integração DB): Conectar o script ao MongoDB para buscar aprovadores dinamicamente.
Fase 3 (Interface): Criar a página no Streamlit para upload do arquivo.
Fase 4 (Validação): Teste com um documento real.
