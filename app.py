import streamlit as st

st.title("NoSQL Databases - Projet")

# Sommaire avec liens cliquables
st.markdown("## Sommaire")
st.page_link("pages/mongo_page.py", label="MongoDB", icon="📂")
st.page_link("pages/neo4j_page.py", label="Neo4j", icon="📂")
st.page_link("pages/transversale_page.py", label="Transversale", icon="📂")