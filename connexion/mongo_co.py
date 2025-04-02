from pymongo import MongoClient
import config
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

def get_mongo_client():
    """
    Crée une instance de client MongoDB à l'aide de l'URI de connexion défini dans le fichier .env.

    Returns:
        MongoClient: Une instance de client MongoDB connecté à la base de données.
    """
    # Se connecter à MongoDB en utilisant l'URI spécifié dans la variable d'environnement MONGO_URI
    return MongoClient(config.MONGO_URI)

def get_database():
    """
    Récupère la base de données 'entertainment' de MongoDB.

    Returns:
        Database: L'instance de la base de données 'entertainment'.
    """
    # Obtient le client MongoDB et se connecte à la base de données 'entertainment'
    client = get_mongo_client()
    return client["entertainment"]

if __name__ == "__main__":   
   # Récupère la base de données MongoDB 'entertainment' et l'assigne à la variable dbname
   dbname = get_database()  
   # Cette étape permet de valider la connexion et d'utiliser la base de données pour d'autres opérations