import streamlit as st
from connexion.transversale_queries import *

st.title("NoSQL Databases - Projet")
st.header("Questions transversales")
st.markdown("")  # Ajoute un saut de ligne
st.markdown("")

st.markdown("#### **Q27. Quels sont les films qui ont des genres en commun mais qui ont des réalisateurs différents ?**")
st.markdown(f"Les films avec des genres en commun mais des réalisateurs différents sont :")
for row in q27():
    film1 = row['Film1']
    realisateur1 = row['Realisateur1']
    film2 = row['Film2']
    realisateur2 = row['Realisateur2']
    genres_communs = ", ".join(row['GenresPartages']) 
    st.markdown(f"- Films : **{film1}** (de {realisateur1}) et **{film2}** (de {realisateur2}) avec **{genres_communs}** comme genre commun.")
st.markdown("---")

st.markdown("#### **Q28. Recommander des films aux utilisateurs en fonction des préférences d'un acteur donné.**")
# Liste des acteurs
acteurs = ["Chris Pratt", "Scarlett Johansson", "Robert Downey Jr.", "Ben Affleck", "Jane Levy", "Robert Pattinson"]

# Créer un menu déroulant (dropdown) pour choisir un acteur
actor_name = st.selectbox("Choisissez un acteur que vous aimez", acteurs)
st.markdown("Voici des films recommandés en fonction de l'acteur choisi :")
st.markdown("\n".join(q28(actor_name)))

st.markdown("#### **Q29. Créer une relation de “concurrence” entre réalisateurs ayant réalisé des films similaires la même année.**")
st.markdown("Voici les relations de concurrence entre réalisateurs ayant réalisé des films similaires la même année :")
# Affichage sous forme de liste
for row in q29():
    realisateur1 = row['Realisateur1']
    realisateur2 = row['Realisateur2']
    film1 = row['Film1']
    film2 = row['Film2']
    year = row['year']
    shared_genres = row['shared_genres']

    st.markdown(f"- Concurrence entre **{realisateur1}** et **{realisateur2}** :")
    st.markdown(f"**Films** : {film1} et {film2}, **Année** : {year}, **Genres partagés** : {', '.join(shared_genres)}")
    st.markdown("")
st.markdown("---")


st.markdown("#### **Q30. Identifier les collaborations les plus fréquentes entre réalisateurs et acteurs, puis analyser si ces collaborations sont associées à un succès commercial ou critique.**")
st.markdown("Voici les collaborations les plus fréquentes entre réalisateurs et acteurs avec leurs succès commercial et critique :")

# Affichage sous forme de liste
for row in q30():
    realisateur = row['Realisateur']
    acteur = row['Acteur']
    collaboration_count = row['collaboration_count']
    ratings = row['ratings']
    total_revenue = row['total_revenue']
    
    # Détermination du succès commercial
    succes_commercial = "**Succès commercial**" if total_revenue > 500 else " **Peu de succès commercial**"

    # Détermination du succès critique
    succes_critique = "**Succès critique**" if any(rating != "G" for rating in ratings) else " **Pas de succès critique**"
    
    st.markdown(f"- Collaboration entre le réalisateur **{realisateur}** et l'acteur **{acteur}** :")
    st.markdown(f"**Nombre de collaborations** : {collaboration_count}, **Liste des notes des films** : {ratings}, **Revenu total des films** : {total_revenue:,.2f}millions d'euros")
    st.markdown(f"{succes_commercial} | {succes_critique}")
    st.markdown("")
st.markdown("---")











