from connexion.neo4j_co import Neo4jConnection

# Récupérer et afficher les films dans Neo4j
conn = Neo4jConnection()


def q27():
    result = conn.query("""MATCH (f1:Films), (f2:Films)
                        WHERE f1 <> f2 AND f1.title < f2.title  // Évite les doublons (A, B) et (B, A)
                        UNWIND split(f1.genre, ',') AS genre1
                        UNWIND split(f2.genre, ',') AS genre2
                        WITH f1, f2, genre1, genre2
                        WHERE genre1 = genre2
                        WITH f1, f2, COLLECT(DISTINCT genre1) AS genres_communs
                        RETURN f1.title AS Film1, f1.director AS Realisateur1, 
                               f2.title AS Film2, f2.director AS Realisateur2, 
                               genres_communs AS GenresPartages
                        LIMIT 10;""") 
    return result


def q28(actor_name):
    result = conn.query("""
    MATCH (a:Actors {name: $actor_name})-[:A_JOUE]->(f:Films)
    UNWIND split(f.genre, ',') AS genre
    MATCH (f2:Films)
    WHERE ANY(g IN split(f2.genre, ',') WHERE g = genre) 
      AND NOT EXISTS { MATCH (a)-[:A_JOUE]->(f2) }
    RETURN DISTINCT f2.title AS RecommendedFilm, f2.genre AS Genre
    LIMIT 5
    """, {"actor_name": actor_name})
    return [f"- {row['RecommendedFilm']}" for row in result]

