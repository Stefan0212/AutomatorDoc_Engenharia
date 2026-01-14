"""
Script para popular o MongoDB com dados iniciais de aprovadores
"""
from db_connection import get_database

def seed_database():
    """
    Popula o banco de dados com dados iniciais de exemplo.
    Usa a estrutura conforme documentação: identifier e approvers.
    """
    try:
        db = get_database()
        collection = db.matrix_configs
        
        # Dados de exemplo baseados na especificação técnica
        # Estrutura conforme documentação: identifier (title_keyword, prefix, aircraft) e approvers
        sample_data = [
            {
                "identifier": {
                    "title_keyword": "CONFIGURATION DOCUMENT",
                    "prefix": "CF",
                    "aircraft": "E2"
                },
                "approvers": {
                    "prepared_by": "Bruno Serpa",
                    "checked_by": "M. Camargo",
                    "approved_by": "Alan Araujo",
                    "industrialization": "Karla Castro",
                    "materials_process": "James Delpinto"
                }
            },
            # Adicione mais documentos conforme necessário
            {
                "identifier": {
                    "title_keyword": "CONFIGURATION DOCUMENT",
                    "prefix": "CF",
                    "aircraft": "E175"
                },
                "approvers": {
                    "prepared_by": "Bruno Serpa",
                    "checked_by": "M. Camargo",
                    "approved_by": "Alan Araujo",
                    "industrialization": "Karla Castro",
                    "materials_process": "James Delpinto"
                }
            }
        ]
        
        # Limpa a coleção (opcional - comentar se quiser manter dados existentes)
        # collection.delete_many({})
        
        # Insere os dados
        for doc in sample_data:
            # Verifica se já existe (evita duplicação)
            existing = collection.find_one({
                "identifier.title_keyword": doc["identifier"]["title_keyword"],
                "identifier.aircraft": doc["identifier"]["aircraft"]
            })
            
            if not existing:
                collection.insert_one(doc)
                print(f"✓ Inserido: {doc['identifier']['title_keyword']} - {doc['identifier']['aircraft']}")
            else:
                print(f"⊘ Já existe: {doc['identifier']['title_keyword']} - {doc['identifier']['aircraft']}")
        
        print("\n✓ População do banco de dados concluída!")
        
    except Exception as e:
        print(f"✗ Erro ao popular o banco de dados: {str(e)}")
        raise


if __name__ == "__main__":
    print("Iniciando população do banco de dados MongoDB...")
    seed_database()
