import streamlit as st
from connexion.mongo_queries import *
from connexion.mongo_co import get_database

db = get_database()  # Récupération de la base de données

st.title("NoSQL Databases - Projet")
st.header("Résultats MongoDB requêtes \n\n")

st.markdown("#### **Q1. Afficher l'année où le plus grand nombre de films ont été sortis.**")
st.markdown(f"L'année avec le plus grand nombre de films sortis est **{q1(db)['_id']}** avec **{q1(db)['count']}** films.")
st.write("---")

st.markdown("#### **Q2. Quel est le nombre de films sortis après l'année 1999.**")
st.markdown(f"Il y a **{q2(db)}** films sortis après 1999.")
st.write("---")

st.markdown("#### **Q3. Quelle est la moyenne des votes des films sortis en 2007.**")
st.markdown(f"La moyenne des votes des films sortis en 2007 est de **{q3(db)}**.")
st.write("---")

st.markdown("#### **Q4. Affichez un histogramme qui permet de visualiser le nombres de films par année.**")
st.write("Histogramme du nombres de films par année : ")
q4(db)
st.write("---")

st.markdown("#### **Q5. Quelles sont les genres de films disponibles dans la base.**")
st.write("Les genres de films disponibles dans la bases :")
st.write("\n".join([f"- **{genre}**" for genre in q5(db)]))
st.write("---")


st.markdown("#### **Q6. Quel est le film qui a généré le plus de revenus.**")
st.markdown(f"Le film qui a généré le plus de revenus est **\"{q6(db)['title']}\"** avec **{q6(db)['Revenue (Millions)']}** millions d'euros de revenus.")
st.write("---")

st.markdown("#### **Q7. Quels sont les réalisateurs ayant réalisé plus de 5 films dans la base de données ?**")
if not q7(db):
    st.write("Il n'y a pas de réalisateurs ayant réalisé plus de 5 films dans la base de données.")
else:
    directors = [d["_id"] for d in q7(db)]  # Extraire les noms des réalisateurs
    st.write("Les réalisateurs ayant réalisé plus de 5 films dans la base de données :", ", ".join(directors))
st.write("---")
    
st.markdown("#### **Q8. Quel est le genre de film qui rapporte en moyenne le plus de revenus ?**")
st.markdown(f"Le genre de film qui rapporte en moyenne le plus de revenus est **\"{q8(db)['_id']}\"** avec **{q8(db)['avg_revenue']}** millions d'euros de revenus en moyenne.")
st.write("---")

st.markdown("#### **Q9. Quels sont les 3 films les mieux notés (rating) pour chaque décennie (1990-1999, 2000-2009, etc.) ?**")
st.write("Les 3 films les mieux notés pour chaque décennie sont :")
for i in range (len(q9(db))):
    decade = q9(db)['decade']
    movies = q9(db)['title']

    st.write(f"**{decade}s**")  # Affichage de la décennie en titre
    for movie in movies:
        st.write(f"- **{movie['title']}** (Note: {movie['rating']})")  # Liste à puces
    st.write("---")    # Séparation
    
st.markdown("#### **Q10. Quel est le film le plus long (Runtime) par genre ?**")
st.write("Le films les plus longs par genre est :")
for i in q10(db):
    genre = i['_id']
    title = i['longest_movie']
    runtime = i['max_runtime']
    st.write(f"- **{genre}** : {title} (**{runtime} min**)")
st.write("---")        
        
st.markdown("#### **Q11. Créer une vue MongoDB affichant uniquement les films ayant une note supérieure à 80 (Metascore) et ayant généré plus de 50 millions de dollars.**")
q11(db)        
st.write("Les films avec un metascore supérieur à 80 et générant plus de 50 millions de dollars sont :")
for film in db.view_q11.find():
    st.write(f"- **{film['title']}** avec un metascore de {film['Metascore']} et {film['Revenue (Millions)']} millions d'euros de revenus.")
st.write("---")  
 
   
st.markdown("#### **Q12. Calculer la corrélation entre la durée des films (Runtime) et leurs revenus (Revenue). (réaliser une analyse statistique.)**")
st.write("Calcul de la corrélation entre la durée des films et leurs revenus")
correlation, p_value = q12(db)
st.write(f"**Corrélation (r)** : {correlation:.2f}")
st.write(f"**P-value** : {p_value:.5f}")
if p_value < 0.05:
    st.markdown("La corrélation est statistiquement significative (p-value < 0.05).")
else:
    st.markdown("La corrélation n'est pas statistiquement significative (p-value >= 0.05).")
st.write("---")  

st.markdown("#### **Q13. Y a-t-il une évolution de la durée moyenne des films par décennie ?**")
st.write("Évolution de la durée moyenne des films par décennie")
for i in q13(db):
    decade = i["_id"]
    avg_runtime = i["avg_runtime"]
    st.write(f"- **{decade}s** : Durée moyenne = {avg_runtime:.2f} minutes")
st.write("On remarque donc que la durée moyenne des films par décennie a diminué entre les années 2000 et 2010 (il n'y a eu qu'un film dans les années 1970).")    
st.write("---")  







        