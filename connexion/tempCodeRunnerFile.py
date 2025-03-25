from neo4j import GraphDatabase
import connexion.config as config
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters).data()

    def close(self):
        self.driver.close()