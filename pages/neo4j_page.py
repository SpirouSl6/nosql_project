import streamlit as st
from connexion.mongo_queries import *
from connexion.neo4j_queries import *
import networkx as nx
import community as community_louvain
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("NoSQL Databases - Projet")
st.header("Résultats Neo4j requêtes")

st.write(f"L'acteur ayant joué dans le plus grand nombre de films est {q14()['a.name']} avec {q14()['FilmCount']} films.")
st.write("---")

actors = [actor['a.name'] for actor in q15()]
st.write(f"Les acteurs ayant joué dans les films où l'actrice Anne Hathaway a également joué sont : {', '.join(actors)}.")
st.write("---")

st.write(f"L'acteur : {q16()['a.name']} a joué dans des films totalisant le plus de revenus avec {q16_2()['TotalRevenue']} euros de revenus pour tous les films.")
st.write("---")

st.write(f"La moyenne des votes sur tous les films est de {q17()}")
st.write("---")

st.write(f"Le genre le plus représenté dans la base de données est {q18()['genre']} avec {q18()['genre_count']} films.")
st.write("---")

st.write(f"Les films dans lesquels les acteurs ayant joué avec moi ont également joué dans : {q19()['fo.title']}")
st.write("---")

st.write(f"Le réalisateur {q20()['d.name']}  a travaillé avec le plus grand nombre d'acteurs distincts : {q20()['NombreActeurs']} acteurs.")
st.write("---")

st.write(f"Les films les plus 'connectés', c'est-`a-dire ceux qui ont le plus d'acteurs en commun avec d'autres films sont : {q21()}")
st.write("---")

st.write(f"Les 5 acteurs ayant joué avec le plus de réalisateurs différents sont : {q22()}")
st.write("---")

st.write(f"Films recommandés à un acteur (Chris Pratt) en fonction des genres des films où il a déjà joué : {q23()}")
st.write("---")

st.write(f"Nombre de relations d'influence : {q24_1()}")

st.write(f"Réalisateurs influencés Kenneth Lonergan : {q24_2()}")
st.write("---")

st.write(f"Le 'chemin' le plus court entre deux acteurs (Daniel Giménez Cacho et Scarlett Johansson) est : {q25()}")
st.write("---")

st.subheader("Communautés d'acteurs selon Louvain")

def q26():
    data = pd.read_csv('q26.csv')

    # Créer un graphe vide
    G = nx.Graph()

    # Ajouter des arêtes entre les acteurs ayant joué ensemble
    for _, row in data.iterrows():
        actor1 = row['Actor1']
        actor2 = row['Actor2']
        common_films = row['CommonFilms']
        G.add_edge(actor1, actor2, weight=common_films)

    # Appliquer l'algorithme Louvain pour détecter les communautés
    partition = community_louvain.best_partition(G)
    
    # Dessiner le graphe en utilisant les communautés
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=50, cmap=plt.cm.jet, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=4)
    plt.title("Communautés d'acteurs selon Louvain")
    
    # Sauvegarder l'image dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    st.image(buf)

    # Diviser les acteurs dans chaque communauté
    communities = {}
    for actor, community_id in partition.items():
        if community_id not in communities:
            communities[community_id] = []
        communities[community_id].append(actor)

    # Afficher les communautés d'acteurs
    community_results = {}
    for community_id, actors in communities.items():
        community_results[community_id] = actors
    
    st.write("Communautés d'acteurs identifiées :")
    st.write(community_results)

    # Créer et afficher un graphe pour chaque communauté
    community_plots = []
    for community_id, actors in communities.items():
        # Sous-graphe pour cette communauté
        subgraph = G.subgraph(actors)
        
        # Créer une liste de couleurs pour les nœuds de ce sous-graphe
        node_colors = [partition[actor] for actor in subgraph.nodes()]

        # Visualiser le sous-graphe
        pos = nx.spring_layout(subgraph)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_nodes(subgraph, pos, node_size=50, cmap=plt.cm.jet, node_color=node_colors)
        nx.draw_networkx_edges(subgraph, pos, alpha=0.5)
        nx.draw_networkx_labels(subgraph, pos, font_size=6)
        plt.title(f"Communauté {community_id} d'acteurs")
        
        # Sauvegarder l'image dans un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        community_plots.append(buf)

    # Afficher les graphiques des communautés dans Streamlit
    for idx, plot in enumerate(community_plots):
        st.image(plot)

# Exécution de q26
q26()

# Fermer la connexion Neo4j
conn.close()























