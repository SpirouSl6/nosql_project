import streamlit as st
from connexion.mongo_queries import *
from connexion.transversale_queries import *
import networkx as nx
import community as community_louvain
import pandas as pd
import matplotlib.pyplot as plt
import io




st.write(f"Films avec des genres en commun mais des réalisateurs différents : {q27()}")


# Liste des acteurs
acteurs = ["Chris Pratt", "Scarlett Johansson", "Robert Downey Jr.", "Ben Affleck", "Jane Levy", "Robert Pattinson"]

# Créer un menu déroulant (dropdown) pour choisir un acteur
actor_name = st.selectbox("Choisissez un acteur", acteurs)
st.write(f"Films recommandés à {actor_name} en fonction de ses genres préférés : {q28(actor_name)}")
















