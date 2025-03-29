import streamlit as st
from connexion.transversale_queries import *


st.write(f"Films avec des genres en commun mais des réalisateurs différents :")
for row in q27():
    film1 = row['Film1']
    realisateur1 = row['Realisateur1']
    film2 = row['Film2']
    realisateur2 = row['Realisateur2']
    genres_communs = ", ".join(row['GenresPartages']) 
    st.write(f"Films : {film1} ({realisateur1}) et {film2} ({realisateur2})")
    st.write(f"Genres communs : {genres_communs}")
    st.write("---")

# Liste des acteurs
acteurs = ["Chris Pratt", "Scarlett Johansson", "Robert Downey Jr.", "Ben Affleck", "Jane Levy", "Robert Pattinson"]

# Créer un menu déroulant (dropdown) pour choisir un acteur
actor_name = st.selectbox("Choisissez un acteur que vous aimez", acteurs)
st.write("Voici des films recommandés en fonction de l'acteur choisi :")
st.markdown("\n".join(q28(actor_name)))
















