from connexion.neo4j_co import Neo4jConnection
from connexion.mongo_co import get_database

# Connexion à Neo4j
conn = Neo4jConnection()
db = get_database()  # Récupération de la base de données

# Fonction pour insérer un film et ses relations dans Neo4j
def noeud_film(film):
    if "title" not in film or "year" not in film or "Director" not in film:
        return  # Ignore ce film si certains champs sont manquants
    
    # Créer le nœud 'Film'
    query = """
    MERGE (f:Film {id: $id})
    SET f.title = $title, f.year = $year, f.votes = $votes, 
        f.revenue = $revenue, f.rating = $rating, f.director = $director
    """
    # Passer les paramètres dans un dictionnaire
    parameters = {
        "id": film["_id"],
        "title": film["title"],
        "year": film["year"],
        "votes": film.get("Votes", 0),
        "revenue": film.get("Revenue (Millions)", 0),
        "rating": film.get("rating", "unrated"),
        "director": film.get("Director", "Unknown")
    }
    conn.query(query, parameters)  # Passer le dictionnaire des paramètres à la méthode query

# Insérer les films depuis MongoDB vers Neo4j
#for film in db.films.find({}, {"_id": 1, "title": 1, "year": 1, 
#                               "Votes": 1, "Revenue (Millions)": 1, 
#                               "rating": 1, "Director": 1}):
#    noeud_film(film)
print("Importation des films terminée avec succès !")






# Fermeture des connexions
conn.close()


