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


st.write("Les genres de films disponibles dans la bases :", ", \n ".join(q5(db)))
st.write("Le film qui a généré le plus de revenus est ", q6(db)['title'], "avec \"", q6(db)['Revenue (Millions)'], "\" millions de revenus.")






