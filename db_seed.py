"""
Script para popular o MongoDB com dados iniciais de aprovadores
"""
from db_connection import get_database

def seed_database():
    """
    Popula o banco de dados com dados iniciais de exemplo.
    """
    try:
        db = get_database()
        collection = db.approvals_matrix
        
        # Dados de exemplo baseados na especificação
        sample_data = [
            {
                "documentTitle_key": "CONFIGURATION DOCUMENT",
                "aircraft_model": "E2",
                "workflow_step": "Engineering Release",
                "approvers": {
                    "prepared_by": "Bruno Serpa",
                    "checked_by": "M. Camargo",
                    "approved_by": "Alan Araujo",
                    "industrialization": "Karla Castro",
                    "mat_process": "James Delpinto"
                },
                "last_update": "2025-01-22"
            },
            # Adicione mais documentos conforme necessário
            {
                "documentTitle_key": "CONFIGURATION DOCUMENT",
                "aircraft_model": "E175",
                "workflow_step": "Engineering Release",
                "approvers": {
                    "prepared_by": "Bruno Serpa",
                    "checked_by": "M. Camargo",
                    "approved_by": "Alan Araujo",
                    "industrialization": "Karla Castro",
                    "mat_process": "James Delpinto"
                },
                "last_update": "2025-01-22"
            }
        ]
        
        # Limpa a coleção (opcional - comentar se quiser manter dados existentes)
        # collection.delete_many({})
        
        # Insere os dados
        for doc in sample_data:
            # Verifica se já existe (evita duplicação)
            existing = collection.find_one({
                "documentTitle_key": doc["documentTitle_key"],
                "aircraft_model": doc["aircraft_model"]
            })
            
            if not existing:
                collection.insert_one(doc)
                print(f"✓ Inserido: {doc['documentTitle_key']} - {doc['aircraft_model']}")
            else:
                print(f"⊘ Já existe: {doc['documentTitle_key']} - {doc['aircraft_model']}")
        
        print("\n✓ População do banco de dados concluída!")
        
    except Exception as e:
        print(f"✗ Erro ao popular o banco de dados: {str(e)}")
        raise


if __name__ == "__main__":
    print("Iniciando população do banco de dados MongoDB...")
    seed_database()
