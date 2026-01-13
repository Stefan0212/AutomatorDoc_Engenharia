"""
Aplicação Streamlit principal - AutomatorDoc
Sistema de automação de preenchimento de documentação técnica
"""
import streamlit as st
from excel_handler import (
    extract_document_info,
    process_excel_file,
    read_excel_file
)
from db_connection import get_approvers
import traceback

# Configuração da página
st.set_page_config(
    page_title="AutomatorDoc - Engenharia Safran",
    page_icon="📄",
    layout="wide"
)

# Título e descrição
st.title("📄 AutomatorDoc - Engenharia Safran")
st.markdown("""
Sistema de automação para preenchimento de documentação técnica.
Faça o upload do arquivo Excel modelo para preencher automaticamente a aba Approvals.
""")


def main():
    """
    Função principal da aplicação
    """
    # Upload do arquivo
    uploaded_file = st.file_uploader(
        "Selecione o arquivo Excel (.xlsx)",
        type=["xlsx"],
        help="Faça o upload do template padrão do documento"
    )
    
    if uploaded_file is not None:
        try:
            # Lê o conteúdo do arquivo
            file_content = uploaded_file.read()
            
            # Carrega o workbook para extrair informações
            workbook = read_excel_file(file_content)
            
            # Extrai informações do documento
            with st.spinner("Analisando o documento..."):
                document_title_key, aircraft_model = extract_document_info(workbook)
            
            # Exibe informações extraídas
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Document Title:** {document_title_key or 'Não encontrado'}")
            with col2:
                st.info(f"**Aircraft Model:** {aircraft_model or 'Não encontrado'}")
            
            if not document_title_key or not aircraft_model:
                st.warning("⚠️ Não foi possível identificar o tipo de documento ou modelo da aeronave. Verifique se as células E15 e E23 na aba Cover estão preenchidas.")
                return
            
            # Busca os aprovadores no banco de dados
            with st.spinner("Buscando aprovadores no banco de dados..."):
                approvers_data = get_approvers(document_title_key, aircraft_model)
            
            if approvers_data is None:
                st.error(f"❌ Nenhum registro encontrado para:\n- Document Title: {document_title_key}\n- Aircraft Model: {aircraft_model}\n\nPor favor, verifique se os dados estão cadastrados no banco de dados.")
                
                # Opção para preenchimento manual (futuro)
                with st.expander("💡 Dica"):
                    st.markdown("""
                    Se você precisar cadastrar novos dados, execute o script `db_seed.py` 
                    ou adicione manualmente no MongoDB na coleção `approvals_matrix`.
                    """)
                return
            
            # Exibe os aprovadores encontrados
            st.success("✅ Aprovadores encontrados no banco de dados!")
            
            with st.expander("👥 Visualizar aprovadores encontrados"):
                approvers = approvers_data.get("approvers", {})
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Prepared by:**", approvers.get("prepared_by", "-"))
                    st.write("**Checked by:**", approvers.get("checked_by", "-"))
                    st.write("**Approved by:**", approvers.get("approved_by", "-"))
                
                with col2:
                    st.write("**Industrialization:**", approvers.get("industrialization", "-"))
                    st.write("**Material Process:**", approvers.get("mat_process", "-"))
            
            # Botão para processar
            if st.button("🔄 Processar e Preencher Documento", type="primary", use_container_width=True):
                try:
                    with st.spinner("Processando o arquivo..."):
                        # Processa o arquivo
                        processed_file = process_excel_file(file_content, approvers_data)
                    
                    st.success("✅ Arquivo processado com sucesso!")
                    
                    # Gera nome do arquivo de saída
                    original_filename = uploaded_file.name
                    if "." in original_filename:
                        name, ext = original_filename.rsplit(".", 1)
                        output_filename = f"{name}_processado.{ext}"
                    else:
                        output_filename = f"{original_filename}_processado.xlsx"
                    
                    # Botão de download
                    st.download_button(
                        label="📥 Baixar Arquivo Processado",
                        data=processed_file,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"❌ Erro ao processar o arquivo: {str(e)}")
                    with st.expander("🔍 Detalhes do erro"):
                        st.code(traceback.format_exc())
        
        except ValueError as e:
            st.error(f"❌ {str(e)}")
        except Exception as e:
            st.error(f"❌ Erro inesperado: {str(e)}")
            with st.expander("🔍 Detalhes do erro"):
                st.code(traceback.format_exc())


def sidebar_info():
    """
    Informações adicionais na barra lateral
    """
    with st.sidebar:
        st.header("ℹ️ Informações")
        st.markdown("""
        ### Como usar:
        1. Faça o upload do arquivo Excel modelo
        2. O sistema identificará automaticamente o tipo de documento
        3. Os aprovadores serão buscados no banco de dados
        4. Baixe o arquivo processado
        
        ### Requisitos:
        - Arquivo deve ter as abas: **Cover** e **Approvals**
        - A célula E15 (Cover) deve conter o Document Title
        - A célula E23 (Cover) deve conter o Aircraft Model
        """)
        
        st.header("🔧 Status do Sistema")
        try:
            db = get_database()
            db.admin.command('ping')
            st.success("✅ MongoDB conectado")
        except Exception as e:
            st.error(f"❌ MongoDB desconectado\n{str(e)}")
        
        st.markdown("---")
        st.markdown("**AutomatorDoc v1.0**\n\nEngenharia Safran")


if __name__ == "__main__":
    # Adiciona informações na sidebar
    sidebar_info()
    
    # Executa a aplicação principal
    main()
