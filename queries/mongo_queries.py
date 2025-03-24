import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy.stats as stats

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
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}]
    result = list(db.films.aggregate(pipeline))
    return result[0]["avg_rating"]


def q4(db):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}]
    data = list(db.films.aggregate(pipeline))
    years = [d["_id"] for d in data]    # Liste des années
    counts = [d["count"] for d in data]   # Liste des nombres de films

    sns.barplot(x=years, y=counts)  #Crée un histogramme
    plt.xlabel("Année")
    plt.ylabel("Nombre de films")
    plt.title("Nombre de films par année")
    plt.show()

