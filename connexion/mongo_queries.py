import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy.stats as stats
import streamlit as st
from pymongo.errors import OperationFailure

def q1(db):
    """
    Récupère l'année avec le plus grand nombre de films dans la base de données.

    Args:
        db: La base de données MongoDB.

    Returns:
        dict: L'année avec le plus grand nombre de films et le nombre de films.
    """
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},  # Groupe par année et compte les films
        {"$sort": {"count": -1}}, # Trie les résultats par nombre de films décroissant
        {"$limit": 1}] # Limite à 1 pour récupérer l'année avec le plus grand nombre
    result = db.films.aggregate(pipeline)
    return list(result)[0] # Récupère le premier résultat de l'agrégation

def q2(db):
    """
    Compte le nombre de films dont l'année est supérieure à 1999.

    Args:
        db: La base de données MongoDB.

    Returns:
        int: Le nombre de films dont l'année est supérieure à 1999.
    """
    result = db.films.count_documents({"year": {"$gt": 1999}})  # Filtre les films après 1999
    return result


def q3(db):
    """
    Calcule la moyenne des votes pour les films de l'année 2007.

    Args:
        db: La base de données MongoDB.

    Returns:
        float: La moyenne des votes pour les films de 2007.
    """
    pipeline = [
        {"$match": {"year": 2007, "Votes": {"$exists": True, "$ne": None}}}, # Filtre les films de 2007 ayant des votes
        {"$group": {"_id": 0, "avg_votes": {"$avg": "$Votes"}}}] # Calcule la moyenne des votes
    result = list(db.films.aggregate(pipeline))
    return result[0]["avg_votes"]


def q4(db):
    """
    Affiche un graphique des films par année avec leur nombre respectif.

    Args:
        db: La base de données MongoDB.
    """
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}}, # Groupe par année et compte les films
        {"$sort": {"_id": 1}}] # Trie par année
    data = list(db.films.aggregate(pipeline))
    years = [d["_id"] for d in data]    # Liste des années
    counts = [d["count"] for d in data]   # Liste des nombres de films
 
    # Crée un graphique avec matplotlib et seaborn
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=years, y=counts, ax=ax)   #Crée un histogramme
    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de films")
    ax.set_title("Nombre de films par année")

    st.pyplot(fig)  # Affiche le graphique dans Streamlit


def q5(db):
    """
    Récupère la liste des genres de films uniques.

    Args:
        db: La base de données MongoDB.

    Returns:
        list: Liste des genres uniques de films.
    """
    pipeline = [
        {"$project": { "genres": { "$split": ["$genre", ","]}}}, # Sépare la chaîne de genres en tableau
        {"$unwind": "$genres" }, # Décompose la liste en plusieurs documents
        {"$group": { "_id": { "$trim": { "input": "$genres"}}}},  # Supprime les espaces et groupe les genres uniques
        {"$sort": { "_id": 1 }} # Trie en ordre alphabétique
    ]
    
    result = list(db.films.aggregate(pipeline))
    return [d["_id"] for d in result]


def q6(db):
    """
    Récupère le film avec le revenu le plus élevé.

    Args:
        db: La base de données MongoDB.

    Returns:
        dict: Le film avec le revenu le plus élevé.
    """
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$exists": True, "$nin": ["", 0]}}},  # Exclure les valeurs nulles
        {"$sort": {"Revenue (Millions)": -1}},  # Trier par revenu décroissant
        {"$limit": 1},  # Garder uniquement le premier
        {"$project": {"title": 1, "Revenue (Millions)": 1}} # Projeter uniquement le titre et le revenu
    ]
    
    result = list(db.films.aggregate(pipeline))
    return result[0]


def q7(db):
    """
    Récupère les réalisateurs ayant dirigé plus de 5 films, triés par nombre de films.

    Args:
        db: La base de données MongoDB.

    Returns:
        list: Liste des réalisateurs avec le nombre de films dirigés.
    """
    pipeline = [
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}}, # Groupe par réalisateur et compte les films
        {"$match": {"count": {"$gt": 5}}}, # Filtrer ceux ayant dirigé plus de 5 films
        {"$sort": {"count": -1}}, # Trie par nombre de films
        {"$project": {"director": "$_id", "count": 1, "_id": 0}} # Projeter uniquement le nom et le nombre de films
    ]
    return list(db.films.aggregate(pipeline))


def q8(db):
    """
    Récupère le genre ayant le revenu moyen le plus élevé.

    Args:
        db: La base de données MongoDB.

    Returns:
        dict: Le genre avec le revenu moyen le plus élevé.
    """
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$exists": True, "$nin": ["", 0]}}}, # Exclure les valeurs nulles
        {"$project": {"genres": { "$split": ["$genre", ","]}, "Revenue (Millions)": 1}}, # Sépare la chaîne de genres en tableau
        {"$unwind": "$genres"}, # Décompose la liste en plusieurs documents
        {"$group": {"_id": { "$trim": { "input": "$genres"}}, "avg_revenue": {"$avg": "$Revenue (Millions)"}}}, # Calcule la moyenne du revenu par genre
        {"$sort": {"avg_revenue": -1}}, # Trie par revenu moyen décroissant
        {"$limit": 1}  # Limite à 1 genre
    ]
    return list(db.films.aggregate(pipeline))[0]


def q9(db):
    """
    Récupère les films avec une note "G", triés par décennie et par note.

    Args:
        db: La base de données MongoDB.

    Returns:
        list: Liste des films par décennie et note.
    """
    pipeline = [
        {"$match": {"year": {"$exists": True, "$ne": None}, "rating": "G"}}, # Filtrer les films avec une note "G"
        {"$project": {"decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}, "title": 1, "rating": 1}}, # Calculer la décennie
        {"$sort": {"decade": 1, "rating": -1}}, # Trier par décennie et par note décroissante
        {"$group": {"_id": "$decade", "title": {"$push": {"title": "$title", "rating": "$rating"}}}}, # Regrouper les films par décennie
        {"$project": {"decade": "$_id", "title": {"$slice": ["$title", 3]}}} # Limiter les films par décennie à 3
    ]
    return list(db.films.aggregate(pipeline))


def q10(db):
    """
    Récupère le genre avec la durée moyenne la plus longue de films.

    Args:
        db: La base de données MongoDB.

    Returns:
        list: Liste des genres avec la durée la plus longue.
    """
    pipeline = [
        {"$match": {"Runtime (Minutes)": {"$exists": True, "$ne": None}}},  # Filtrer les films sans durée
        {"$project": {"title": 1, "genres": { "$split": ["$genre", ","]}, "runtime": "$Runtime (Minutes)"}}, 
        {"$unwind": "$genres" },  # Décompose la liste en plusieurs documents
        {"$set": {"genres": { "$trim": { "input": "$genres"}}}},  # Supprime les espaces et groupe les genres uniques
        {"$group": {"_id": "$genres", "max_runtime": {"$max": "$runtime"}, "longest_movie": {"$first": "$title"}}}, # Récupère le genre avec la plus longue durée
        {"$sort": {"max_runtime": -1}} # Trie par durée décroissante
    ]
    return list(db.films.aggregate(pipeline))


def q11(db): 
    """
    Crée une vue des films avec un score Metascore supérieur à 80 et un revenu supérieur à 50 millions.

    Args:
        db: La base de données MongoDB.
    """
    pipeline = [{"$match": {"Metascore": {"$gt": 80}, "Revenue (Millions)": {"$gt": 50}}}]
    
    # Supprimer la vue si elle existe déjà
    try:
        db.view_q11.drop()
    except OperationFailure:
        print("La vue 'view_q11' n'existe pas.")
        
    # Création de la vue
    db.command({"create": "view_q11", "viewOn": "films", "pipeline": pipeline})
    

def q12(db):
    """
    Calcule la corrélation de Pearson entre la durée des films et leur revenu.

    Args:
        db: La base de données MongoDB.

    Returns:
        tuple: La corrélation et la p-value entre la durée et le revenu.
    """
    movies = list(db.films.aggregate([{"$match": {"Runtime (Minutes)": {"$exists": True, "$ne": None}}}, {"$project": {"Runtime (Minutes)": 1, "Revenue (Millions)": 1, "_id": 0}}]))
    # Créer le DataFrame
    df = pd.DataFrame(movies)
    # Convertir la colonne 'Revenue (Millions)' en float
    df['Revenue (Millions)'] = pd.to_numeric(df['Revenue (Millions)'], errors='coerce')
    df.dropna(subset=["Runtime (Minutes)", "Revenue (Millions)"], inplace=True)
    correlation, p_value = stats.pearsonr(df["Runtime (Minutes)"], df["Revenue (Millions)"])
    return correlation, p_value

def q13(db):
    """
    Affiche l'évolution de la durée moyenne des films par décennie.

    Args:
        db: La base de données MongoDB.

    Returns:
        list: Liste des décennies et de la durée moyenne des films.
    """
    pipeline = [
        {"$match": {"year": {"$exists": True, "$ne": None}, "Runtime (Minutes)": {"$exists": True, "$ne": None}}}, # Filtrer les films avec année et durée
        {"$project": {"decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}, "runtime": "$Runtime (Minutes)"}},
        {"$group": {"_id": "$decade", "avg_runtime": {"$avg": "$runtime"}}},
        {"$sort": {"_id": 1}} # Trier par décennie
    ]
    data = list(db.films.aggregate(pipeline))
    
    years = [d["_id"] for d in data]    # Liste des années
    time = [d["avg_runtime"] for d in data]   # Liste des nombres de films
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=years, y=time, ax=ax)   #Crée un histogramme
    ax.set_xlabel("Décennie")
    ax.set_ylabel("Durée moyenne (minutes)")
    ax.set_title("Évolution de la durée moyenne des films par décennie")
    st.pyplot(fig)  # Affiche le graphique dans Streamlit
    
    return data