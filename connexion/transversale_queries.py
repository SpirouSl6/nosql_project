from connexion.neo4j_co import Neo4jConnection

# Récupérer et afficher les films dans Neo4j
conn = Neo4jConnection()


def q27():
    """
    Récupère les films ayant des genres partagés et les affiche avec leurs réalisateurs.

    Cette fonction effectue une requête Cypher pour trouver des paires de films ayant des genres communs,
    tout en évitant les doublons (par exemple, (A, B) et (B, A)).
    Elle retourne les titres des films, les réalisateurs et les genres partagés.

    Returns:
        list: Une liste de dictionnaires contenant les titres des films, leurs réalisateurs et les genres partagés.
    """
    # Requête Cypher pour récupérer les films partageant au moins un genre
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
    return result # Retourne la liste des films avec genres partagés et réalisateurs


def q28(actor_name):
    """
    Recommande des films à un acteur en fonction de ses genres préférés.

    Cette fonction effectue une requête Cypher pour recommander des films à un acteur spécifié,
    en fonction des genres de films dans lesquels il a déjà joué, mais sans recommander les films
    auxquels il a déjà participé.

    Args:
        actor_name (str): Le nom de l'acteur pour lequel les recommandations de films sont effectuées.

    Returns:
        list: Une liste de chaînes représentant les titres des films recommandés pour l'acteur.
    """
    # Requête Cypher pour recommander des films basés sur les genres préférés de l'acteur
    result = conn.query("""MATCH (a:Actors {name: $actor_name})-[:A_JOUE]->(f:Films)
                        UNWIND split(f.genre, ',') AS genre
                        MATCH (f2:Films)
                        WHERE ANY(g IN split(f2.genre, ',') WHERE g = genre) 
                        AND NOT EXISTS { MATCH (a)-[:A_JOUE]->(f2) }
                        RETURN DISTINCT f2.title AS RecommendedFilm, f2.genre AS Genre
                        LIMIT 5
                        """, {"actor_name": actor_name})
    return [f"- {row['RecommendedFilm']}" for row in result] # Retourne la liste des films recommandés


def q29():
    """
    Récupère les réalisateurs qui ont réalisé des films dans les mêmes années et genres.

    Cette fonction effectue une requête Cypher pour identifier des réalisateurs ayant travaillé sur des films
    dans la même année et ayant des genres partagés. Elle crée également des relations de concurrence entre ces réalisateurs.

    Returns:
        list: Une liste de dictionnaires contenant les noms des réalisateurs, les titres des films et les genres partagés.
    """
    # Requête Cypher pour identifier les réalisateurs ayant travaillé sur des films similaires
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
    return result # Retourne la liste des réalisateurs et leurs films en concurrence


def q30():
    """
    Récupère les collaborations entre réalisateurs et acteurs, en fonction du nombre de films réalisés et des revenus générés.

    Cette fonction effectue une requête Cypher pour récupérer les réalisateurs ayant collaboré avec des acteurs dans au moins 2 films
    et calcule les revenus totaux générés par ces collaborations. Les résultats sont triés par nombre de collaborations.

    Returns:
        list: Une liste de dictionnaires contenant les noms des réalisateurs, des acteurs, le nombre de collaborations et les revenus totaux.
    """
    # Requête Cypher pour identifier les collaborations fréquentes entre réalisateurs et acteurs
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films)<-[:A_REALISE]-(r:Realisateur)
                           WITH r, a, COUNT(f) AS collaboration_count, SUM(COALESCE(toFloat(f.revenue), 0)) AS total_revenue
                           WHERE collaboration_count >= 2
                           ORDER BY collaboration_count DESC
                           RETURN r.name AS Realisateur, a.name AS Acteur, collaboration_count, total_revenue""")
    return result # Retourne la liste des collaborations entre réalisateurs et acteurs


# Fermeture de la connexion à la base de données Neo4j
conn.close()