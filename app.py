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
from db_connection import get_approvers, get_database
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
            
            if not document_title_key or not aircraft_model:
                st.warning("⚠️ Não foi possível identificar o tipo de documento ou modelo da aeronave. Verifique se os rótulos 'DOCUMENT TITLE:' e 'AIRCRAFT MODEL:' estão presentes na aba Cover.")
                return
            
            # Dashboard de Diagnóstico
            st.success("✅ Informações identificadas com sucesso!")
            st.markdown("### 📊 Dashboard de Diagnóstico")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📄 **Documento identificado:** {document_title_key}")
            with col2:
                st.info(f"✈️ **Modelo identificado:** {aircraft_model}")
            
            # Busca os aprovadores no banco de dados
            with st.spinner("Buscando aprovadores no banco de dados..."):
                approvers_data = get_approvers(document_title_key, aircraft_model)
            
            if approvers_data is None:
                st.warning("⚠️ Nenhum registro encontrado no banco de dados. Você pode preencher manualmente os campos abaixo.")
                approvers_default = {
                    "prepared_by": "",
                    "checked_by": "",
                    "approved_by": "",
                    "industrialization": "",
                    "materials_process": ""
                }
            else:
                approvers_default = approvers_data.get("approvers", {})
            
            # Painel de Validação (Preview) - Campos editáveis
            st.markdown("### ✏️ Painel de Validação")
            st.markdown("Revise e edite os nomes dos aprovadores se necessário:")
            
            # Campos de texto editáveis
            prepared_by = st.text_input(
                "Campo 1 - Prepared By",
                value=approvers_default.get("prepared_by", ""),
                key="prepared_by"
            )
            
            checked_by = st.text_input(
                "Campo 2 - Checked By",
                value=approvers_default.get("checked_by", ""),
                key="checked_by"
            )
            
            approved_by = st.text_input(
                "Campo 3 - Approved By",
                value=approvers_default.get("approved_by", ""),
                key="approved_by"
            )
            
            industrialization = st.text_input(
                "Campo 4 - Industrialization",
                value=approvers_default.get("industrialization", ""),
                key="industrialization"
            )
            
            materials_process = st.text_input(
                "Campo 5 - Materials Process",
                value=approvers_default.get("materials_process", ""),
                key="materials_process"
            )
            
            # Prepara os dados dos aprovadores com os valores editados
            approvers_final = {
                "approvers": {
                    "prepared_by": prepared_by,
                    "checked_by": checked_by,
                    "approved_by": approved_by,
                    "industrialization": industrialization,
                    "materials_process": materials_process
                }
            }
            
            # Botão de processamento
            st.markdown("---")
            if st.button("🚀 Gerar Documento Final", type="primary", use_container_width=True):
                # Validação: verifica se pelo menos um campo foi preenchido
                if not any([prepared_by, checked_by, approved_by, industrialization, materials_process]):
                    st.error("❌ Por favor, preencha pelo menos um campo de aprovador.")
                else:
                    try:
                        with st.spinner("Processando o arquivo..."):
                            # Processa o arquivo com os valores validados/editados
                            processed_file = process_excel_file(file_content, approvers_final)
                        
                        st.success("✅ Arquivo processado com sucesso!")
                        
                        # Gera nome do arquivo de saída
                        original_filename = uploaded_file.name
                        if "." in original_filename:
                            name, ext = original_filename.rsplit(".", 1)
                            output_filename = f"{name}_PREENCHIDO.{ext}"
                        else:
                            output_filename = f"{original_filename}_PREENCHIDO.xlsx"
                        
                        # Área de Download
                        st.markdown("### ⬇️ Área de Download")
                        st.download_button(
                            label=f"📥 Download: {output_filename}",
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
        - A aba Cover deve conter os rótulos: **DOCUMENT TITLE:** e **AIRCRAFT MODEL:**
        - Os valores devem estar nas células à direita dos rótulos
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
