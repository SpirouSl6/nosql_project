import streamlit as st
from queries.mongo_queries import *
from database.mongo import get_database

db = get_database()  # Récupération de la base de données

st.title("NoSQL Databases - Projet")
st.header("Requêtes MongoDB")

result_q1 = q1(db)
st.write("Année avec le plus grand nombre de films sortis :", result_q1[0]['_id'], "avec", result_q1[0]['count'], "films.")
st.write("Nombre de films sortis après 1999 :", q2(db))

