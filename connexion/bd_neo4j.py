from neo4j_co import Neo4jConnection
from mongo_co import get_database

# Connexion à Neo4j
conn = Neo4jConnection() # Initialisation de la connexion à la base Neo4j
db = get_database()  # Récupération de la base de données

# Fonction pour insérer un nœud 'Film' dans Neo4j
def noeud_film(film):
    """
    Crée ou met à jour un nœud 'Film' dans Neo4j avec les informations fournies.

    Parameters:
        film (dict): Dictionnaire contenant les informations du film, avec des clés comme "title", "year", "Director", etc.
    """
    if "title" not in film or "year" not in film or "Director" not in film:
        return  # Ignore ce film si certains champs sont manquants
    
    # Requête pour insérer ou mettre à jour un nœud 'Film'
    query = """
    MERGE (f:Films {id: $id})
    SET f.title = $title, f.year = $year, f.votes = $votes, 
        f.revenue = $revenue, f.rating = $rating, f.director = $director, f.genre = $genre
    """
    # Paramètres de la requête
    parameters = {
        "id": film["_id"],
        "title": film["title"],
        "year": film["year"],
        "genre": film["genre"],
        "votes": film.get("Votes", 0),
        "revenue": film.get("Revenue (Millions)", 0),
        "rating": film.get("rating", "unrated"),
        "director": film.get("Director", "Unknown")
    }
    conn.query(query, parameters)  # Exécution de la requête


# Fonction pour insérer un nœud 'Actor' dans Neo4j
def noeud_actor(actor_name):
    """
    Crée un nœud 'Actor' dans Neo4j pour l'acteur spécifié.

    Parameters:
        actor_name (str): Nom de l'acteur à ajouter dans Neo4j.
    """
    query = """
    MERGE (a:Actors {name: $name})
    """
    parameters = {"name": actor_name.strip()} # Suppression des espaces superflus
    conn.query(query, parameters) # Exécution de la requête


# Fonction pour insérer une relation "A joué" entre un acteur et un film
def relation_a_joue(actor_name, film_id):
    """
    Crée une relation 'A_JOUE' entre un acteur et un film dans Neo4j.

    Parameters:
        actor_name (str): Nom de l'acteur.
        film_id (str): Identifiant du film.
    """
    query = """
    MATCH (a:Actors {name: $name}), (f:Films {id: $id})
    MERGE (a)-[:A_JOUE]->(f)
    """
    parameters = {"name": actor_name.strip(), "id": film_id} # Paramètres de la relation
    conn.query(query, parameters)


# Fonction pour insérer une relation "A réalisé" entre un réalisateur et un film
def relation_a_realiser(director_name, film_id):
    """
    Crée une relation 'A_REALISE' entre un réalisateur et un film dans Neo4j.

    Parameters:
        director_name (str): Nom du réalisateur.
        film_id (str): Identifiant du film.
    """
    query = """
    MATCH (f:Films {id: $id})
    MERGE (d:Realisateur {name: $director_name})
    MERGE (d)-[:A_REALISE]->(f);
    """
    parameters = {"id": film_id, "director_name": director_name.strip()} # Paramètres de la relation
    conn.query(query, parameters)
    

# Fonction pour insérer des relations 'INFLUENCE_PAR' entre réalisateurs ayant réalisé des films du même genre
def relation_influence_par():
    """
    Crée des relations 'INFLUENCE_PAR' entre les réalisateurs qui ont réalisé des films du même genre.
    """
    query = """
    MATCH (d1:Realisateur)-[:A_REALISE]->(f1:Films)
    MATCH (d2:Realisateur)-[:A_REALISE]->(f2:Films)
    WHERE d1 <> d2 
    AND ANY(genre IN f1.genre WHERE genre IN f2.genre)
    MERGE (d1)-[:INFLUENCE_PAR]->(d2);
    """
    conn.query(query)
          
            
# Fonction pour ajouter un acteur spécifique (Sarah Rialland Tardy) au film "Guardians of the Galaxy"
def add_actor_me():
    """
    Ajoute un acteur (Sarah Rialland Tardy) et le lie au film "Guardians of the Galaxy".
    """
    noeud_actor("Sarah Rialland Tardy") # Crée un nœud acteur
    film = db.films.find_one({"title": "Guardians of the Galaxy"}) # Recherche le film par titre
    # Crée la relation 'A joué' entre l'acteur et le film
    relation_a_joue("Sarah Rialland Tardy", film["_id"])
    print("Nœud créé")


# Fonction pour insérer un nœud 'Realisateur' dans Neo4j
def noeud_director(director_name):
    """
    Crée un nœud 'Realisateur' dans Neo4j pour le réalisateur spécifié.

    Parameters:
        director_name (str): Nom du réalisateur.
    """
    query = """
    MERGE (a:Realisateur {name: $name})
    """
    parameters = {"name": director_name.strip()}
    conn.query(query, parameters)
    
# Fonction pour importer les films, acteurs, réalisateurs et relations depuis MongoDB vers Neo4j                
def importation():
    """
    Importe des films, acteurs, réalisateurs et relations depuis MongoDB vers Neo4j.
    """
    # Insérer les films depuis MongoDB vers Neo4j
    for film in db.films.find({}, {"_id": 1, "title": 1, "year": 1, 
                                "Votes": 1, "Revenue (Millions)": 1, 
                                "rating": 1, "Director": 1, "genre": 1}):
        noeud_film(film) # Insère chaque film dans Neo4j
    print("Importation des films terminée !")
    
    # Insérer les acteurs et les relations 'A joué'
    for actor in db.films.aggregate([
            {"$project": {"_id": 1, "title": 1, "year": 1, "Votes": 1, "Revenue (Millions)": 1, "rating": 1, "Director": 1, "genre": 1, "Actors": { "$split": [{"$replaceAll": {"input": "$Actors", "find" : ", ", "replacement": ","}},","]}}}, 
            {"$unwind": "$Actors"}, 
            {"$set": {"Actors": { "$trim": { "input": "$Actors"}}}}]):
        actor_name = actor["Actors"]
        film_id = actor["_id"]

        noeud_actor(actor_name)  # Création du nœud acteur
        relation_a_joue(actor_name, film_id)  # Création de la relation acteur-film
    print("Importation des acteurs et relations terminée !")
    print("Création des relations 'A joué' terminée !")
    
    add_actor_me() # Ajoute moi comme acteur et crée la relation avec un film spécifique
    
    # Insérer les réalisateurs et les relations 'A réalisé'
    for director in db.films.find({}, {"_id": 0, "Director": 1}):
        if director.get("Director"):
            noeud_director(director["Director"]) # Création du nœud réalisateur
    print("Importation des directors terminée !")
    
    # Créer des relations 'A réalisé' pour chaque film
    for film in db.films.find({}, {"_id": 1, "title": 1, "Director": 1}):
        if "Director" in film and film["Director"]:
            relation_a_realiser(film["Director"], film["_id"]) # Créer la relation 'A réalisé' entre réalisateur et film
    print("Création des relations 'A_REALISE' terminée !")
    
    relation_influence_par() # Crée des relations d'influence entre réalisateurs
    print("Création des relations 'INFLUENCE_PAR' terminée !")


importation() # Exécute l'importation

# Fermeture de la connexion à Neo4j
conn.close()