from connexion.neo4j_co import Neo4jConnection

# Récupérer et afficher les films dans Neo4j
conn = Neo4jConnection()


def q28(actor_name):
    result = conn.query("""
    MATCH (a:Actors {name: $actor_name})-[:A_JOUE]->(f:Films)
    UNWIND split(f.genre, ',') AS genre
    MATCH (f2:Films)
    WHERE ANY(g IN split(f2.genre, ',') WHERE g = genre) AND NOT EXISTS {
    MATCH (a)-[:A_JOUE]->(f2)}
    RETURN f2.title AS RecommendedFilm, f2.genre AS Genre
    LIMIT 5
    """, actor_name=actor_name)
    return result

