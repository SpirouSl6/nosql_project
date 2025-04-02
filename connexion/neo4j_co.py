from neo4j import GraphDatabase
from dotenv import load_dotenv
import sys
import os

# Ajouter le répertoire racine au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

load_dotenv() # Charge les variables d'environnement depuis le fichier .env

class Neo4jConnection:
    """
    Classe de connexion à une base de données Neo4j. Permet d'exécuter des requêtes Cypher
    et de gérer la connexion à la base de données.
    """
    def __init__(self):
        """
        Initialise la connexion à la base de données Neo4j en utilisant les informations de connexion
        fournies dans le fichier de configuration (config.py).
        
        Charge l'URI, l'utilisateur et le mot de passe à partir des variables d'environnement
        définies dans le fichier .env.
        """
        # Création du driver de connexion Neo4j en utilisant les informations stockées dans config.py
        self.driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))

    def query(self, query, parameters=None):
        """
        Exécute une requête Cypher sur la base de données Neo4j et retourne les résultats.
        
        Args:
            query (str): La requête Cypher à exécuter.
            parameters (dict, optional): Un dictionnaire de paramètres à utiliser dans la requête Cypher. Par défaut, None.

        Returns:
            list: Une liste de résultats sous forme de dictionnaires.
        """
        # Ouverture d'une session Neo4j pour exécuter la requête
        with self.driver.session() as session:
            # Exécution de la requête Cypher avec les paramètres éventuels et récupération des résultats
            return session.run(query, parameters).data()

    def close(self):
        """
        Ferme la connexion au driver Neo4j. Cette méthode doit être appelée lorsque la connexion n'est plus nécessaire
        pour libérer les ressources.
        """
        # Fermeture de la connexion Neo4j pour libérer les ressources
        self.driver.close()