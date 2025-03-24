import streamlit as st
from database.mongo import get_database


st.title("Exploration de bases de données NoSQL")

db = get_database()

st.header("Année avec le plus grand nombre de films")

