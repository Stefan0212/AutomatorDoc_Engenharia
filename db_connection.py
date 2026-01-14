"""
Módulo de conexão com MongoDB
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

# Configurações do banco de dados
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "technical_docs")

# Cliente MongoDB
_client = None
_db = None


def get_database():
    """
    Retorna uma instância do banco de dados MongoDB.
    Utiliza singleton pattern para reutilizar a conexão.
    """
    global _client, _db
    
    if _db is None:
        try:
            _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Testa a conexão
            _client.admin.command('ping')
            _db = _client[DB_NAME]
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            raise ConnectionError(f"Erro ao conectar ao MongoDB: {str(e)}")
    
    return _db


def close_connection():
    """
    Fecha a conexão com o MongoDB.
    """
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None


def get_approvers(document_title_key, aircraft_model):
    """
    Busca os aprovadores no MongoDB baseado no tipo de documento e modelo de aeronave.
    Usa a estrutura conforme documentação: identifier.title_keyword e identifier.aircraft
    
    Args:
        document_title_key (str): Palavra-chave do título do documento (normalizado em upper)
        aircraft_model (str): Modelo da aeronave (normalizado em upper)
    
    Returns:
        dict: Dicionário com os aprovadores ou None se não encontrado
    """
    try:
        db = get_database()
        collection = db.matrix_configs
        
        # Estrutura conforme documentação: identifier.title_keyword e identifier.aircraft
        # Também tenta buscar pelo prefixo "CF" se o título contém "CONFIGURATION DOCUMENT"
        query = {
            "identifier.title_keyword": document_title_key,
            "identifier.aircraft": aircraft_model
        }
        
        result = collection.find_one(query)
        
        if result:
            # Remove o _id do MongoDB do resultado
            result.pop("_id", None)
            return result
        
        return None
    except Exception as e:
        raise Exception(f"Erro ao buscar aprovadores: {str(e)}")
