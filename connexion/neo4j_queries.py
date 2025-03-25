from neo4j_co import Neo4jConnection

# Récupérer et afficher les films dans Neo4j
conn = Neo4jConnection()

# Exécuter la requête pour récupérer les films
films = conn.query("MATCH (f:Film) RETURN f LIMIT 10")  # Récupérer 10 films

# Afficher les résultats
for film in films:
    print(film)

# Fermer la connexion
conn.close()