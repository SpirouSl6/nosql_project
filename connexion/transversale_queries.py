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


def q29():
    result = conn.query("""MATCH (d1:Realisateur)-[:A_REALISE]->(f1:Films)
                            MATCH (d2:Realisateur)-[:A_REALISE]->(f2:Films)
                            WHERE f1 <> f2 AND f1.year = f2.year 
                            WITH f1, f2, d1, d2
                            UNWIND split(f1.genre, ',') AS genre1
                            UNWIND split(f2.genre, ',') AS genre2
                            WITH f1, f2, d1, d2, genre1, genre2
                            WHERE genre1 = genre2  
                            WITH d1, d2, COLLECT(DISTINCT genre1) AS shared_genres, f1, f2
                            MERGE (d1)-[:CONCURRENCE]->(d2)
                            RETURN d1.name AS Realisateur1, d2.name AS Realisateur2, 
                                   f1.title AS Film1, f2.title AS Film2, 
                                   f1.year AS year, shared_genres
                            LIMIT 10;""") 
    return result


def q30():
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films)<-[:A_REALISE]-(r:Realisateur)
                           WITH r, a, COUNT(f) AS collaboration_count, COLLECT(f.rating) AS ratings, SUM(COALESCE(toFloat(f.revenue), 0)) AS total_revenue
                           WHERE collaboration_count >= 2
                           ORDER BY collaboration_count DESC
                           RETURN r.name AS Realisateur, a.name AS Acteur, collaboration_count, ratings, total_revenue""")
    return result