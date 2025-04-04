import streamlit as st
from connexion.mongo_queries import *
from connexion.mongo_co import get_database

db = get_database()  # Récupération de la base de données

# Titre de l'application Streamlit
st.title("NoSQL Databases - Projet")
st.header("Résultats MongoDB requêtes")
st.markdown("")  # Ajoute un saut de ligne pour l'affichage
st.markdown("") 

st.markdown("#### **Q1. Afficher l'année où le plus grand nombre de films ont été sortis.**")
st.markdown(f"L'année avec le plus grand nombre de films sortis est en **{q1(db)['_id']}** avec **{q1(db)['count']}** films.")
st.markdown("---")

st.markdown("#### **Q2. Quel est le nombre de films sortis après l'année 1999 ?**")
st.markdown(f"Il y a **{q2(db)}** films sortis après 1999.")
st.markdown("---")

st.markdown("#### **Q3. Quelle est la moyenne des votes des films sortis en 2007 ?**")
st.markdown(f"La moyenne des votes des films sortis en 2007 est de **{q3(db)}**.")
st.markdown("---")

st.markdown("#### **Q4. Affichez un histogramme qui permet de visualiser le nombre de films par année.**")
st.markdown("Histogramme du nombre de films par année : ")
q4(db)
st.markdown("---")

st.markdown("#### **Q5. Quelles sont les genres de films disponibles dans la base ?**")
st.markdown("Les genres de films disponibles dans la base sont :")
st.markdown("\n".join([f"- **{genre}**" for genre in q5(db)]))
st.markdown("---")


st.markdown("#### **Q6. Quel est le film qui a généré le plus de revenus ?**")
st.markdown(f"Le film qui a généré le plus de revenus est **\"{q6(db)['title']}\"** avec **{q6(db)['Revenue (Millions)']}** millions d'euros de revenus.")
st.markdown("---")

st.markdown("#### **Q7. Quels sont les réalisateurs ayant réalisé plus de 5 films dans la base de données ?**")
if not q7(db):
    st.markdown("Il n'y a pas de réalisateurs ayant réalisé plus de 5 films dans la base de données.")
else:
    directors = [d["_id"] for d in q7(db)]  # Extraire les noms des réalisateurs
    st.markdown("Les réalisateurs ayant réalisé plus de 5 films dans la base de données :", ", ".join(directors))
st.markdown("---")
    
st.markdown("#### **Q8. Quel est le genre de film qui rapporte en moyenne le plus de revenus ?**")
st.markdown(f"Le genre de film qui rapporte en moyenne le plus de revenus est **\"{q8(db)['_id']}\"** avec **{round(q8(db)['avg_revenue'], 2)}** millions d'euros de revenus en moyenne.")
st.markdown("---")

st.markdown("#### **Q9. Quels sont les 3 films les mieux notés (rating) pour chaque décennie (1990-1999, 2000-2009, etc.) ?**")
st.markdown("Les 3 films les mieux notés pour chaque décennie sont :")
for result in q9(db):
    decade = result['decade']
    movies = result['title']

    st.markdown(f"**{decade}s**")  # Affichage de la décennie en titre
    for movie in movies:
        st.markdown(f"- **{movie['title']}** (Note: {movie['rating']})")  # Liste à puces
    st.markdown("---")    # Séparation
    
st.markdown("#### **Q10. Quel est le film le plus long (Runtime) par genre ?**")
st.markdown("Le film le plus long par genre est :")
for i in q10(db):
    genre = i['_id']
    title = i['longest_movie']
    runtime = i['max_runtime']
    st.markdown(f"- **{genre}** : {title} (**{runtime} min**)")
st.markdown("---")        
        
st.markdown("#### **Q11. Créer une vue MongoDB affichant uniquement les films ayant une note supérieure à 80 (Metascore) et ayant généré plus de 50 millions de dollars.**")
q11(db)        
st.markdown("Les films avec un metascore supérieur à 80 et générant plus de 50 millions de dollars sont :")
for film in db.view_q11.find():
    st.markdown(f"- **{film['title']}** avec un metascore de {film['Metascore']} et {film['Revenue (Millions)']} millions d'euros de revenus.")
st.markdown("---")  
 
   
st.markdown("#### **Q12. Calculer la corrélation entre la durée des films (Runtime) et leurs revenus (Revenue). (réaliser une analyse statistique.)**")
st.markdown("Calcul de la corrélation entre la durée des films et leurs revenus")
correlation, p_value = q12(db)
st.markdown(f"**Corrélation (r)** : {correlation:.2f}")
st.markdown(f"**P-value** : {p_value:.5f}")
# Interprétation des résultats
if p_value < 0.05:
    if correlation > 0:
        st.markdown("La corrélation est **positive** et statistiquement significative (p-value < 0.05). Cela signifie que les films plus longs ont **tendance à générer plus de revenus**.")
    elif correlation < 0:
        st.markdown("La corrélation est **négative** et statistiquement significative (p-value < 0.05). Cela signifie que les films plus longs ont **tendance à générer moins de revenus**.")
    else:
        st.markdown("Bien que statistiquement significative, la corrélation est **très faible**, ce qui signifie qu'il n'y a pas de lien clair entre la durée des films et leurs revenus.")
else:
    st.markdown("La corrélation **n'est pas statistiquement significative** (p-value >= 0.05). Cela signifie que l'on **ne peut pas conclure** à une relation fiable entre la durée des films et leurs revenus.")
st.markdown("---")  

st.markdown("#### **Q13. Y a-t-il une évolution de la durée moyenne des films par décennie ?**")
st.markdown("Évolution de la durée moyenne des films par décennie")
decade_runtimes = {}
for i in q13(db):
    decade = i["_id"]
    avg_runtime = i["avg_runtime"]
    decade_runtimes[decade] = avg_runtime
    st.markdown(f"- **{decade}s** : Durée moyenne = {avg_runtime:.2f} minutes")
    
if decade_runtimes[2010] < decade_runtimes[2000]:
    st.markdown("On remarque donc que la durée moyenne des films par décennie a **diminué** entre les années 2000 et 2010 (il n'y a eu qu'un film dans les années 1970).")
else:
    st.markdown("On remarque donc que la durée moyenne des films par décennie a **augmenté** entre les années 2000 et 2010 (il n'y a eu qu'un film dans les années 1970).")
st.markdown("---")  