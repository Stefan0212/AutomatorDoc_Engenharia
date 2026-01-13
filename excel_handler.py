"""
Módulo para manipulação de arquivos Excel
"""
from openpyxl import load_workbook
from openpyxl.styles import Font
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

# Senha do Excel (se necessário)
EXCEL_PASSWORD = os.getenv("EXCEL_PASSWORD", None)

# Mapeamento de células para a aba Approvals
APPROVALS_MAPPING = {
    "prepared_by": "E5",
    "checked_by": "F5",
    "approved_by": "G5",
    "industrialization": "H5",
    "mat_process": "I5"
}

# Células de referência na aba Cover
COVER_DOCUMENT_TITLE = "E15"  # DOCUMENT TITLE
COVER_AIRCRAFT_MODEL = "E23"  # AIRCRAFT MODEL


def read_excel_file(file_content):
    """
    Carrega um arquivo Excel a partir de conteúdo em bytes.
    
    Args:
        file_content (bytes): Conteúdo do arquivo Excel
    
    Returns:
        openpyxl.Workbook: Workbook carregado
    """
    try:
        workbook = load_workbook(
            filename=BytesIO(file_content),
            data_only=False,  # Preserva fórmulas
            keep_vba=True  # Mantém macros
        )
        return workbook
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo Excel: {str(e)}")


def extract_document_info(workbook):
    """
    Extrai informações do documento da aba Cover.
    
    Args:
        workbook (openpyxl.Workbook): Workbook do Excel
    
    Returns:
        tuple: (document_title_key, aircraft_model)
    """
    try:
        if "Cover" not in workbook.sheetnames:
            raise ValueError("A aba 'Cover' não foi encontrada no arquivo Excel")
        
        cover_sheet = workbook["Cover"]
        
        # Lê o Document Title (E15)
        document_title_key = cover_sheet[COVER_DOCUMENT_TITLE].value
        if document_title_key:
            document_title_key = str(document_title_key).strip()
        
        # Lê o Aircraft Model (E23)
        aircraft_model = cover_sheet[COVER_AIRCRAFT_MODEL].value
        if aircraft_model:
            aircraft_model = str(aircraft_model).strip()
        
        return document_title_key, aircraft_model
    except Exception as e:
        raise Exception(f"Erro ao extrair informações do documento: {str(e)}")


def fill_approvals_sheet(workbook, approvers_data):
    """
    Preenche a aba Approvals com os dados dos aprovadores.
    
    Args:
        workbook (openpyxl.Workbook): Workbook do Excel
        approvers_data (dict): Dicionário com os dados dos aprovadores
    
    Returns:
        openpyxl.Workbook: Workbook atualizado
    """
    try:
        if "Approvals" not in workbook.sheetnames:
            raise ValueError("A aba 'Approvals' não foi encontrada no arquivo Excel")
        
        approvals_sheet = workbook["Approvals"]
        approvers = approvers_data.get("approvers", {})
        
        # Define a fonte padrão (Arial, tamanho 11)
        default_font = Font(name="Arial", size=11)
        
        # Preenche as células mapeadas
        for field, cell_address in APPROVALS_MAPPING.items():
            if field in approvers:
                cell = approvals_sheet[cell_address]
                cell.value = approvers[field]
                # Aplica a formatação
                cell.font = default_font
        
        return workbook
    except Exception as e:
        raise Exception(f"Erro ao preencher a aba Approvals: {str(e)}")


def save_workbook_to_bytes(workbook):
    """
    Salva o workbook em memória (BytesIO) para download.
    
    Args:
        workbook (openpyxl.Workbook): Workbook do Excel
    
    Returns:
        bytes: Conteúdo do arquivo Excel em bytes
    """
    try:
        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        raise Exception(f"Erro ao salvar o arquivo Excel: {str(e)}")


def process_excel_file(file_content, approvers_data):
    """
    Processa um arquivo Excel completo: lê, preenche e retorna os bytes.
    
    Args:
        file_content (bytes): Conteúdo do arquivo Excel original
        approvers_data (dict): Dicionário com os dados dos aprovadores
    
    Returns:
        bytes: Conteúdo do arquivo Excel processado
    """
    workbook = read_excel_file(file_content)
    workbook = fill_approvals_sheet(workbook, approvers_data)
    return save_workbook_to_bytes(workbook)
