import streamlit as st
from connexion.mongo_queries import *
from connexion.mongo_co import get_database

db = get_database()  # Récupération de la base de données

st.title("NoSQL Databases - Projet")
st.header("Résultats MongoDB requêtes")

st.markdown("<h2 style='font-weight: bold;'>Afficher l’année où le plus grand nombre de films ont été sortis.</h2>", unsafe_allow_html=True)
st.write("Année avec le plus grand nombre de films sortis : ", q1(db)['_id'],  "avec", q1(db)['count'], "films.")
st.write("---")

st.write("Nombre de films sortis après 1999 : ", q2(db))
st.write("---")

st.write("Moyenne des votes des films sortis en 2007 : ", q3(db))
st.write("---")

st.write("Histogramme nombres de films par année : ")
q4(db)
st.write("---")

st.write("Les genres de films disponibles dans la bases :", ", ".join(q5(db)))
st.write("---")

st.write("Le film qui a généré le plus de revenus est **\"{}\"** avec **{}** millions d'euros de revenus.".format(q6(db)["title"], q6(db)["Revenue (Millions)"]))
st.write("---")


if not q7(db):
    st.write("Il n'y a pas de réalisateurs ayant réalisé plus de 5 films dans la base de données.")
else:
    directors = [d["_id"] for d in q7(db)]  # Extraire les noms des réalisateurs
    st.write("Les réalisateurs ayant réalisé plus de 5 films dans la base de données :", ", ".join(directors))
st.write("---")
    
st.write("Le genre de film qui rapporte en moyenne le plus de revenus est **\"{}\"** avec **{}** millions d'euros de revenus en moyenne.".format(q8(db)["_id"], q8(db)["avg_revenue"]))
st.write("---")

st.write("### Les 3 films les mieux notés pour chaque décennie :")
for i in range (len(q9(db))):
    decade = q9(db)['decade']
    movies = q9(db)['title']

    st.write(f"#### {decade}s")  # Affichage de la décennie en titre
    for movie in movies:
        st.write(f"- **{movie['title']}** (Note: {movie['rating']})")  # Liste à puces
    st.write("---")    # Séparation
    

st.write("### Films les plus longs par genre")
for i in q10(db):
    genre = i['_id']
    title = i['longest_movie']
    runtime = i['max_runtime']
    st.write(f"- **{genre}** : {title} (**{runtime} min**)")
st.write("---")        
        

q11(db)        
st.write("### Films avec un metascore supérieur à 80 et générant plus de 50 millions de dollars:")
for film in db.view_q11.find():
    st.write(f"**{film['title']}**")
    st.write(f"Metascore: {film['Metascore']}")
    st.write(f"Revenue: {film['Revenue (Millions)']} millions d'euros")
    st.write("---")  
   

st.write("### Calcul de la corrélation entre la durée des films et leur revenu")
correlation, p_value = q12(db)
st.write(f"**Corrélation (r)** : {correlation:.2f}")
st.write(f"**P-value** : {p_value:.5f}")
if p_value < 0.05:
    st.markdown("La corrélation est statistiquement significative (p-value < 0.05).")
else:
    st.markdown("La corrélation n'est pas statistiquement significative (p-value >= 0.05).")
st.write("---")  


st.write("### Évolution de la durée moyenne des films par décennie")
for i in q13(db):
    decade = i["_id"]
    avg_runtime = i["avg_runtime"]
    st.write(f"- **{decade}s** : Durée moyenne = {avg_runtime:.2f} minutes")
st.write("---")  







        