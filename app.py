import streamlit as st
from queries.mongo_queries import *
from database.mongo import get_database

db = get_database()  # Récupération de la base de données

st.sidebar.header("Test de connexion MongoDB")

if db:
    try:
        collections = db.list_collection_names()
        st.sidebar.success("Connexion réussie à MongoDB ✅")
        st.sidebar.write(f"Collections disponibles : {collections}")
    except Exception as e:
        st.sidebar.error(f"Erreur d'accès aux collections : {e}")
else:
    st.sidebar.error("Connexion à MongoDB échouée ❌")

