from neo4j_co import Neo4jConnection
from mongo_co import get_database

# Connexion à Neo4j
conn = Neo4jConnection()
db = get_database()  # Récupération de la base de données

# Fonction pour insérer les films
def noeud_film(film):
    if "title" not in film or "year" not in film or "Director" not in film:
        return  # Ignore ce film si certains champs sont manquants
    
    # Créer le nœud 'Film'
    query = """
    MERGE (f:Films {id: $id})
    SET f.title = $title, f.year = $year, f.votes = $votes, 
        f.revenue = $revenue, f.rating = $rating, f.director = $director, f.genre = $genre
    """
    # Passer les paramètres dans un dictionnaire
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
    conn.query(query, parameters)  # Passer le dictionnaire des paramètres à la méthode query


# Fonction pour insérer les acteurs
def noeud_actor(actor_name):
    query = """
    MERGE (a:Actors {name: $name})
    """
    parameters = {"name": actor_name.strip()}
    conn.query(query, parameters)


# Fonction pour insérer les relations "A joué"
def relation_a_joue(actor_name, film_id):
    query = """
    MATCH (a:Actors {name: $name}), (f:Films {id: $id})
    MERGE (a)-[:A_JOUE]->(f)
    """
    parameters = {"name": actor_name.strip(), "id": film_id}
    conn.query(query, parameters)


# Fonction pour insérer les relations "A réaliser"
def relation_a_realiser(director_name, film_id):
    query = """
    MATCH (f:Films {id: $id})
    MERGE (d:Realisateur {name: $director_name})
    MERGE (d)-[:A_REALISE]->(f);
    """
    parameters = {"id": film_id, "director_name": director_name.strip()}
    conn.query(query, parameters)
    

# Fonction pour insérer les relations "A réaliser"
def relation_influence_par():
    query = """
    MATCH (d1:Realisateur)-[:A_REALISE]->(f1:Films)
    MATCH (d2:Realisateur)-[:A_REALISE]->(f2:Films)
    WHERE d1 <> d2 
    AND ANY(genre IN f1.genre WHERE genre IN f2.genre)
    MERGE (d1)-[:INFLUENCE_PAR]->(d2);
    """
    conn.query(query)
          
            
# Création du nœud acteur et relation avec le film
def add_actor_me():
    noeud_actor("Sarah Rialland Tardy")
    film = db.films.find_one({"title": "Guardians of the Galaxy"})
    # Relier "Sarah Rialland Tardy" au film "Guardians of the Galaxy"
    relation_a_joue("Sarah Rialland Tardy", film["_id"])
    print("Nœud créé")


# Fonction pour insérer les acteurs
def noeud_director(director_name):
    query = """
    MERGE (a:Realisateur {name: $name})
    """
    parameters = {"name": director_name.strip()}
    conn.query(query, parameters)
    
                
def importation():
    # Insérer les films depuis MongoDB vers Neo4j
    for film in db.films.find({}, {"_id": 1, "title": 1, "year": 1, 
                                "Votes": 1, "Revenue (Millions)": 1, 
                                "rating": 1, "Director": 1, "genre": 1}):
        noeud_film(film)
    print("Importation des films terminée !")
    
    # Insérer les films depuis MongoDB vers Neo4j
    for actor in db.films.aggregate([
            {"$project": {"_id": 1, "title": 1, "year": 1, "Votes": 1, "Revenue (Millions)": 1, "rating": 1, "Director": 1, "genre": 1, "Actors": { "$split": [{"$replaceAll": {"input": "$Actors", "find" : ", ", "replacement": ","}},","]}}}, 
            {"$unwind": "$Actors"}, 
            {"$set": {"Actors": { "$trim": { "input": "$Actors"}}}}]):
        actor_name = actor["Actors"]
        film_id = actor["_id"]

        noeud_actor(actor_name)  # Création du nœud acteur
        relation_a_joue(actor_name, film_id)  # Création de la relation
    print("Importation des acteurs et relations terminée !")
    print("Création des relations 'A joué' terminée !")
    
    add_actor_me()
    
    # Insérer les films depuis MongoDB vers Neo4j
    for director in db.films.find({}, {"_id": 0, "Director": 1}):
        if director.get("Director"):
            noeud_director(director["Director"])
    print("Importation des directors terminée !")
    
    for film in db.films.find({}, {"_id": 1, "title": 1, "Director": 1}):
        if "Director" in film and film["Director"]:
            relation_a_realiser(film["Director"], film["_id"])
    print("Création des relations 'A_REALISE' terminée !")
    
    relation_influence_par()
    print("Création des relations 'INFLUENCE_PAR' terminée !")


importation()
# Fermeture des connexions
conn.close()

    
    

