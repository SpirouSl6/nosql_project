import streamlit as st
from queries.mongo_queries import *
from database.mongo import get_database

db = get_database()  # Récupération de la base de données

st.title("NoSQL Databases - Projet")
st.header("Requêtes MongoDB")

st.write("Nombre total de documents :", db.films.count_documents({}))
st.write("Année avec le plus grand nombre de films sortis : ", q1(db)['_id'],  "avec", q1(db)['count'], "films.")
st.write("Nombre de films sortis après 1999 : ", q2(db))
st.write("Moyenne des votes des films sortis en 2007. : ", q3(db))
st.write("Histogramme nombres de films par année : ", q4(db))










