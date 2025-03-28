from connexion.neo4j_co import Neo4jConnection

# Récupérer et afficher les films dans Neo4j
conn = Neo4jConnection()



def q27():
    result = conn.query("""
    MATCH (f1:Films)-[:A_REALISE]->(d1:Realisateur), (f2:Films)-[:A_REALISE]->(d2:Realisateur)
    WHERE f1 <> f2 AND d1 <> d2
    WITH f1, f2, d1, d2, split(f1.genre, ',') AS genres_f1, split(f2.genre, ',') AS genres_f2
    UNWIND genres_f1 AS genre1
    UNWIND genres_f2 AS genre2
    WHERE genre1 = genre2
    RETURN f1.title AS Film1, f2.title AS Film2, genre1 AS Genre
    """)
    return result


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

