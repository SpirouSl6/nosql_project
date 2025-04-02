from connexion.neo4j_co import Neo4jConnection

# Création de l'instance de connexion à la base de données Neo4j
conn = Neo4jConnection()

def q14():
    """
    Récupère l'acteur ayant joué dans le plus grand nombre de films.

    Effectue une requête Cypher pour compter le nombre de films dans lesquels chaque acteur a joué,
    puis retourne l'acteur avec le plus grand nombre de films.
    
    Returns:
        dict: Un dictionnaire contenant le nom de l'acteur et le nombre de films dans lesquels il a joué.
    """
    # Requête Cypher qui compte les films par acteur et trie pour récupérer celui avec le plus grand nombre
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films) 
                        RETURN a.name, COUNT(f) AS FilmCount 
                        ORDER BY FilmCount DESC 
                        LIMIT 1""") 
    return result[0] # Retourne le premier acteur trouvé avec le plus grand nombre de films

def q15():
    """
    Récupère l'acteur ayant joué dans le plus grand nombre de films.

    Effectue une requête Cypher pour compter le nombre de films dans lesquels chaque acteur a joué,
    puis retourne l'acteur avec le plus grand nombre de films.
    
    Returns:
        dict: Un dictionnaire contenant le nom de l'acteur et le nombre de films dans lesquels il a joué.
    """
    # Requête Cypher pour récupérer les acteurs ayant joué avec Anne Hathaway
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films)<-[:A_JOUE]-(ah:Actors {name: 'Anne Hathaway'}) 
                        RETURN a.name""") 
    return result # Retourne la liste des acteurs ayant joué avec Anne Hathaway


def q16():
    """
    Récupère l'acteur ayant généré le plus de revenus grâce à ses films.

    Effectue une requête Cypher pour calculer le revenu total généré par chaque acteur
    à partir de ses films, puis retourne l'acteur avec le revenu le plus élevé.
    
    Returns:
        dict: Un dictionnaire contenant le nom de l'acteur et son revenu total.
    """
    # Requête Cypher pour calculer le revenu total de chaque acteur
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films) 
                        WITH a, SUM(COALESCE(toFloat(f.revenue), 0)) AS TotalRevenue 
                        RETURN a.name, TotalRevenue 
                        ORDER BY TotalRevenue DESC 
                        LIMIT 1""") 
    return result[0] # Retourne l'acteur ayant généré le plus de revenu

def q17():
    """
    Récupère l'acteur ayant généré le plus de revenus grâce à ses films.

    Effectue une requête Cypher pour calculer le revenu total généré par chaque acteur
    à partir de ses films, puis retourne l'acteur avec le revenu le plus élevé.
    
    Returns:
        dict: Un dictionnaire contenant le nom de l'acteur et son revenu total.
    """
    # Requête Cypher pour calculer la moyenne des votes des films
    result = conn.query("""MATCH (f:Films) 
                        RETURN AVG(f.votes)""") 
    return result[0]['AVG(f.votes)'] # Retourne la moyenne des votes

def q18():
    """
    Récupère le genre de film le plus fréquent.

    Effectue une requête Cypher pour compter le nombre de films par genre,
    puis retourne le genre de film le plus fréquent.
    
    Returns:
        dict: Un dictionnaire contenant le genre de film et son nombre d'occurrences.
    """
    # Requête Cypher pour compter les genres de films
    result = conn.query("""MATCH (f:Films) 
                        UNWIND split(f.genre, ',') AS genre 
                        RETURN genre, COUNT(*) AS genre_count 
                        ORDER BY genre_count DESC 
                        LIMIT 1""") 
    return result[0] # Retourne le genre le plus fréquent

def q19():
    """
    Récupère les films dans lesquels les autres acteurs ont joué avec Sarah Rialland Tardy.

    Effectue une requête Cypher pour trouver les films dans lesquels Sarah Rialland Tardy a joué avec d'autres acteurs.
    
    Returns:
        list: Une liste des titres des films où Sarah Rialland Tardy a joué avec d'autres acteurs.
    """
    # Requête Cypher pour trouver les films avec Sarah Rialland Tardy et d'autres acteurs
    result = conn.query("""MATCH (a:Actors {name: 'Sarah Rialland Tardy'})-[:A_JOUE]->(f:Films)<-[:A_JOUE]-(other:Actors)-[:A_JOUE]->(fo:Films) 
                        WHERE other.name <> a 
                        RETURN fo.title""") 
    return result # Retourne les titres des films où Sarah Rialland Tardy a joué avec d'autres acteurs

def q20():
    """
    Récupère le réalisateur ayant travaillé avec le plus grand nombre d'acteurs.

    Effectue une requête Cypher pour compter le nombre d'acteurs distincts ayant travaillé avec chaque réalisateur,
    puis retourne le réalisateur avec le plus grand nombre d'acteurs.
    
    Returns:
        dict: Un dictionnaire contenant le nom du réalisateur et le nombre d'acteurs distincts.
    """
    # Requête Cypher pour compter le nombre d'acteurs distincts par réalisateur
    result = conn.query("""MATCH (d:Realisateur)-[:A_REALISE]->(f:Films)<-[:A_JOUE]-(a:Actors)
                        RETURN d.name, COUNT(DISTINCT a) AS NombreActeurs
                        ORDER BY NombreActeurs DESC
                        LIMIT 1;""") 
    return result[0] # Retourne le réalisateur avec le plus grand nombre d'acteurs

def q21():
    """
    Récupère les films qui ont été joués par les mêmes acteurs.

    Effectue une requête Cypher pour trouver les films connectés à d'autres films par des acteurs communs,
    puis retourne les films avec le plus grand nombre de films connectés.
    
    Returns:
        list: Une liste de dictionnaires contenant les titres des films et le nombre de films connectés.
    """
    # Requête Cypher pour trouver les films connectés par des acteurs communs
    result = conn.query("""MATCH (f1:Films)<-[:A_JOUE]-(a:Actors)-[:A_JOUE]->(f2:Films)
                        WHERE f1 <> f2
                        WITH f1, COUNT(DISTINCT f2) AS NombreFilmsConnectes
                        RETURN f1.title, NombreFilmsConnectes
                        ORDER BY NombreFilmsConnectes DESC
                        LIMIT 5;""") 
    return result # Retourne les films connectés à d'autres films

def q22():
    """
    Récupère les acteurs ayant travaillé avec le plus grand nombre de réalisateurs.

    Effectue une requête Cypher pour compter le nombre de réalisateurs distincts ayant travaillé avec chaque acteur,
    puis retourne les 5 acteurs ayant travaillé avec le plus grand nombre de réalisateurs.
    
    Returns:
        list: Une liste de dictionnaires contenant les noms des acteurs et le nombre de réalisateurs distincts.
    """
    # Requête Cypher pour compter le nombre de réalisateurs distincts pour chaque acteur
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films)<-[:A_REALISE]-(d:Realisateur)
                        RETURN a.name, COUNT(DISTINCT d) AS NombreRealisateurs
                        ORDER BY NombreRealisateurs DESC
                        LIMIT 5;""") 
    return result # Retourne les 5 acteurs ayant travaillé avec le plus grand nombre de réalisateurs

def q23():
    """
    Recommande un film à Chris Pratt en fonction de ses genres préférés.

    Effectue une requête Cypher pour trouver les genres de films préférés de Chris Pratt,
    puis recommande un film non joué par Chris Pratt, mais qui appartient à un de ses genres préférés.
    
    Returns:
        dict: Un dictionnaire contenant le titre et le genre du film recommandé.
    """
    # Requête Cypher pour recommander un film basé sur les genres préférés de Chris Pratt
    result = conn.query("""MATCH (a:Actors {name: "Chris Pratt"})-[:A_JOUE]->(f:Films)
                        UNWIND split(f.genre, ',') AS genre 
                        WITH a, collect(DISTINCT genre) AS genres_pref
                        MATCH (f2:Films)
                        WHERE ANY(genre IN genres_pref WHERE genre IN f2.genre)
                        AND NOT EXISTS { MATCH (a)-[:A_JOUE]->(f2) }  
                        RETURN f2.title, f2.genre
                        LIMIT 1;""") 
    return result[0] # Retourne le film recommandé à Chris Pratt

def q24_1():
    """
    Récupère le nombre total de relations d'influence entre réalisateurs.

    Effectue une requête Cypher pour compter le nombre de relations d'influence entre réalisateurs.
    
    Returns:
        dict: Un dictionnaire contenant le nombre total de relations d'influence.
    """
    # Requête Cypher pour compter les relations d'influence entre réalisateurs
    result = conn.query("""MATCH ()-[r:INFLUENCE_PAR]->()
                        RETURN count(r);""") 
    return result[0] # Retourne le nombre total de relations d'influence

def q24_2():
    """
    Récupère les réalisateurs influencés par Kenneth Lonergan.

    Effectue une requête Cypher pour trouver tous les réalisateurs ayant été influencés par Kenneth Lonergan.
    
    Returns:
        list: Une liste de dictionnaires contenant les noms des réalisateurs influencés par Kenneth Lonergan.
    """
    # Requête Cypher pour trouver les réalisateurs influencés par Kenneth Lonergan
    result = conn.query("""MATCH (d1:Realisateur)-[:INFLUENCE_PAR]->(d2:Realisateur {name: "Kenneth Lonergan"})
                        RETURN d1.name;""") 
    return result # Retourne les réalisateurs influencés par Kenneth Lonergan


def q25():
    """
    Trouve le chemin le plus court entre deux acteurs (Daniel Giménez Cacho et Scarlett Johansson).

    Effectue une requête Cypher pour trouver le plus court chemin entre les acteurs Daniel Giménez Cacho et Scarlett Johansson
    en utilisant les films dans lesquels ils ont joué.
    
    Returns:
        dict: Un dictionnaire contenant le chemin le plus court entre les deux acteurs.
    """
    # Requête Cypher pour trouver le plus court chemin entre les deux acteurs
    result = conn.query("""MATCH p = shortestPath((a1:Actors {name: "Daniel Giménez Cacho"})-[*..10]-(a2:Actors {name: "Scarlett Johansson"}))
                        RETURN p;""") 
    return result[0] # Retourne le chemin le plus court entre les deux acteurs


# Ferme la connexion à la base de données Neo4j
conn.close()