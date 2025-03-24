import streamlit as st
from queries.mongo_queries import *
from database.mongo import get_database

db = get_database()  # Récupération de la base de données
fdb = db["films"]

st.title("NoSQL Databases - Projet")
st.header("Requêtes MongoDB")

print(fdb.count_documents())
#st.write("Année avec le plus grand nombre de films sortis :", q1(fdb)['_id'], "avec", q1(fdb)['count'], "films.")
#st.write("Nombre de films sortis après 1999 :", q2(fdb))