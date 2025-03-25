import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy.stats as stats
import streamlit as st
from pymongo.errors import OperationFailure

def q1(db):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}]
    result = db.films.aggregate(pipeline)
    return list(result)[0]

def q2(db):
    result = db.films.count_documents({"year": {"$gt": 1999}})
    return result


def q3(db):
    pipeline = [
        {"$match": {"year": 2007, "rating": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": 0, "avg_rating": {"$avg": "$rating"}}}]
    result = list(db.films.aggregate(pipeline))
    return result[0]["avg_rating"]


def q4(db):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}]
    data = list(db.films.aggregate(pipeline))
    years = [d["_id"] for d in data]    # Liste des années
    counts = [d["count"] for d in data]   # Liste des nombres de films
 
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=years, y=counts, ax=ax)   #Crée un histogramme
    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de films")
    ax.set_title("Nombre de films par année")

    st.pyplot(fig)  # Affiche le graphique dans Streamlit


def q5(db):
    pipeline = [
        {"$project": { "genres": { "$split": ["$genre", ","]}}}, # Sépare la chaîne de genres en tableau
        {"$unwind": "$genres" },                                    # Décompose la liste en plusieurs documents
        {"$group": { "_id": { "$trim": { "input": "$genres"}}}},  # Supprime les espaces et groupe les genres uniques
        {"$sort": { "_id": 1 }}                                     # Trie en ordre alphabétique
    ]
    
    result = list(db.films.aggregate(pipeline))
    return [d["_id"] for d in result]


def q6(db):
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$exists": True, "$nin": ["", 0]}}},  # Exclure les valeurs nulles
        {"$sort": {"Revenue (Millions)": -1}},  # Trier par revenu décroissant
        {"$limit": 1},  # Garder uniquement le premier
        {"$project": {"title": 1, "Revenue (Millions)": 1}} 
    ]
    
    result = list(db.films.aggregate(pipeline))
    return result[0]


def q7(db):
    pipeline = [
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}},
        {"$sort": {"count": -1}},
        {"$project": {"director": "$_id", "count": 1, "_id": 0}}
    ]
    return list(db.films.aggregate(pipeline))


def q8(db):
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$exists": True, "$nin": ["", 0]}}},
        {"$project": {"genres": { "$split": ["$genre", ","]}, "Revenue (Millions)": 1}}, # Sépare la chaîne de genres en tableau
        {"$unwind": "$genres"},
        {"$group": {"_id": { "$trim": { "input": "$genres"}}, "avg_revenue": {"$avg": "$Revenue (Millions)"}}},
        {"$sort": {"avg_revenue": -1}},
        {"$limit": 1}
    ]
    return list(db.films.aggregate(pipeline))[0]


def q9(db):
    pipeline = [
        {"$match": {"year": {"$exists": True, "$ne": None}, "rating": "G"}},
        {"$project": {"decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}, "title": 1, "rating": 1}},
        {"$sort": {"decade": 1, "rating": -1}},
        {"$group": {"_id": "$decade", "title": {"$push": {"title": "$title", "rating": "$rating"}}}},
        {"$project": {"decade": "$_id", "title": {"$slice": ["$title", 3]}}}
    ]
    return list(db.films.aggregate(pipeline))[0]


def q10(db):
    pipeline = [
        {"$match": {"Runtime (Minutes)": {"$exists": True, "$ne": None}}},  # Filtrer les films sans durée
        {"$project": {"title": 1, "genres": { "$split": ["$genre", ","]}, "runtime": "$Runtime (Minutes)"}}, 
        {"$unwind": "$genres" },                                    # Décompose la liste en plusieurs documents
        {"$set": {"genres": { "$trim": { "input": "$genres"}}}},  # Supprime les espaces et groupe les genres uniques
        {"$group": {"_id": "$genres", "max_runtime": {"$max": "$runtime"}, "longest_movie": {"$first": "$title"}}},
        {"$sort": {"max_runtime": -1}}
    ]
    return list(db.films.aggregate(pipeline))


def q11(db): 
    pipeline = [{"$match": {"Metascore": {"$gt": 80}, "Revenue (Millions)": {"$gt": 50}}}]
    
    # Supprimer la vue si elle existe déjà
    try:
        db.view_q11.drop()
        print("Vue 'view_q11' supprimée")
    except OperationFailure:
        print("La vue 'view_q11' n'existe pas.")
        
    # Création de la vue
    db.command({"create": "view_q11", "viewOn": "films", "pipeline": pipeline})
    print(f"Vue 'view_q11' créée avec succès !")
    

def q12(db):
    movies = list(db.films.aggregate([{"$match": {"Runtime (Minutes)": {"$exists": True, "$ne": None}}}, {"$project": {"Runtime (Minutes)": 1, "Revenue (Millions)": 1, "_id": 0}}]))
    # Vérifier si des films ont été trouvés
    if len(movies) == 0:
        print("Aucun film trouvé avec les champs 'Runtime (Minutes)' et 'Revenue (Millions)'.")
        return None, None

    # Créer le DataFrame
    df = pd.DataFrame(movies)
    print("Colonnes dans le DataFrame :", df.columns)
    
    print("Extrait des données :")
    print(df.head())
    print("Types des colonnes :")
    print(df.dtypes)

    if 'Runtime (Minutes)' not in df.columns or 'Revenue (Millions)' not in df.columns:
        print("Les colonnes 'Runtime (Minutes)' ou 'Revenue (Millions)' sont manquantes dans les données.")
        return None, None

    df.dropna(subset=["Runtime (Minutes)", "Revenue (Millions)"], inplace=True)
    if len(df) == 0:
        print("Aucune donnée valide pour le calcul de la corrélation.")
        return None, None
    correlation, p_value = stats.pearsonr(df["Runtime (Minutes)"], df["Revenue (Millions)"])
    
    return correlation, p_value

def q13(db):
    pipeline = [
        {"$match": {"year": {"$exists": True, "$ne": None}, "Runtime (Minutes)": {"$exists": True, "$ne": None}}},
        {"$project": {"decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}, "runtime": "$Runtime (Minutes)"}},
        {"$group": {"_id": "$decade", "avg_runtime": {"$avg": "$runtime"}}},
        {"$sort": {"_id": 1}}
    ]
    return list(db.films.aggregate(pipeline))[0]

