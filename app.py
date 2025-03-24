import streamlit as st
from queries.mongo_queries import *

st.title("NoSQL Databases - Projet")
st.header("Requêtes MongoDB")

st.write("Année avec le plus grand nombre de films sortis :", q1()["year"])
st.write("Nombre de films sortis après 1999 :", q2())

