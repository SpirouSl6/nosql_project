import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy.stats as stats
import streamlit as st

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
    genres = db.films.distinct("genre")  # Récupère les chaînes de genres uniques
    genre_set = set()  # Utilisation d'un ensemble pour éviter les doublons

    for genre_str in genres:
        genre_list = genre_str.split(",")  # Sépare les genres dans les chaînes de caractères
        genre_set.update(g.strip() for g in genre_list)  # Nettoie et ajoute les genres

    return genre_set


def q6(db):
    return db.films.find_one({}, sort=[("Revenue", -1)], projection={"title": 1, "Revenue": 1})

















