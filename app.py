import streamlit as st
from queries.mongo_queries import *
from database.mongo import get_database

db = get_database()  # Récupération de la base de données

st.title("NoSQL Databases - Projet")
st.header("Requêtes MongoDB")

st.write("Année avec le plus grand nombre de films sortis : ", q1(db)['_id'],  "avec", q1(db)['count'], "films.")
st.write("Nombre de films sortis après 1999 : ", q2(db))
st.write("Moyenne des votes des films sortis en 2007 : ", q3(db))
st.write("Histogramme nombres de films par année : ")
q4(db)


st.write("Les genres de films disponibles dans la bases :", ", ".join(q5(db)))
st.write("Le film qui a généré le plus de revenus est **\"{}\"** avec **{}** millions d'euros de revenus.".format(q6(db)["title"], q6(db)["Revenue (Millions)"]))


if not q7(db):
    st.write("Il n'y a pas de réalisateurs ayant réalisé plus de 5 films dans la base de données.")
else:
    directors = [d["_id"] for d in q7(db)]  # Extraire les noms des réalisateurs
    st.write("Les réalisateurs ayant réalisé plus de 5 films dans la base de données :", ", ".join(directors))
    
st.write("Le genre de film qui rapporte en moyenne le plus de revenus est **\"{}\"** avec **{}** millions d'euros de revenus en moyenne.".format(q8(db)["_id"], q8(db)["avg_revenue"]))


st.write("### Les 3 films les mieux notés pour chaque décennie :")
for entry in q9(db):
    decade = entry["decade"]
    movies = entry["title"]

    st.write(f"#### {decade}s")  # Affichage de la décennie en titre
    for movie in movies:
        st.write(f"- **{movie['title']}** (Note: {movie['rating']})")  # Liste à puces
    st.write("---")  # Séparation entre les décennies
    

st.write("### Films les plus longs par genre")
for entry in q10(db):
    genre = entry["_id"]
    title = entry["longest_movie"]
    runtime = entry["max_runtime"]
    st.write(f"- **{genre}** : {title} (**{runtime} min**)")
        
        
        
        
        
        
        
        