import os
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv(".env")

# Charger l'URI depuis les variables d'environnement
MONGO_URI = os.getenv("MONGO_URI")

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")