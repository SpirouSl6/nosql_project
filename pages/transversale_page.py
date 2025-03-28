import streamlit as st
from connexion.transversale_queries import *


#st.write(f"Films avec des genres en commun mais des réalisateurs différents : {q27()}")


# Liste des acteurs
acteurs = ["Chris Pratt", "Scarlett Johansson", "Robert Downey Jr.", "Ben Affleck", "Jane Levy", "Robert Pattinson"]

# Créer un menu déroulant (dropdown) pour choisir un acteur
actor_name = st.selectbox("Choisissez un acteur que vous aimez", acteurs)
st.write("### Voici des films recommandés en fonction de l'acteur choisi :")
st.markdown("\n".join(q28(actor_name)))
















