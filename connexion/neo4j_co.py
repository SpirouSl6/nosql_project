from neo4j import GraphDatabase
from dotenv import load_dotenv
import sys
import os

# Ajouter le répertoire racine au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters).data()

    def close(self):
        self.driver.close()