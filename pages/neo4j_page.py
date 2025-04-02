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
st.write("")  # Ajoute un saut de ligne
st.write("") 

st.markdown("#### **Q14. Quel est l'acteur ayant joué dans le plus grand nombre de films ?**")
st.write(f"L'acteur ayant joué dans le plus grand nombre de films est **{q14()['a.name']}** avec **{q14()['FilmCount']}** films.")
st.write("---")

st.markdown("#### **Q15. Quels sont les acteurs ayant joué dans des films où l'actrice Anne Hathaway a également joué ?**")
st.write(f"Les acteurs ayant joué dans les films où l'actrice Anne Hathaway a également joué sont :")
st.write("\n".join([f"- **{actor['a.name']}**" for actor in q15()]))
st.write("---")

st.markdown("#### **Q16. Quel est l'acteur ayant joué dans des films totalisant le plus de revenus ?**")
st.write(f"L'acteur **{q16()['a.name']}** a joué dans des films totalisant le plus de revenus avec **{q16()['TotalRevenue']}** euros de revenus pour tous les films.")
st.write("---")

st.markdown("#### **Q17. Quelle est la moyenne des votes ?**")
st.write(f"La moyenne des votes sur tous les films est de **{round(q17(), 2)}**.")
st.write("---")

st.markdown("#### **Q18. Quel est le genre le plus représenté dans la base de données ?**")
st.write(f"Le genre le plus représenté dans la base de données est **{q18()['genre']}** avec **{q18()['genre_count']}** films.")
st.write("---")

st.markdown("#### **Q19. Quels sont les films dans lesquels les acteurs ayant joué avec vous ont également joué ?**")
st.write(f"Les films dans lesquels les acteurs ayant joué avec moi ont également joué dans :")
st.write("\n".join([f"- **{title['fo.title']}**" for title in q19()]))
st.write("---")

st.markdown("#### **Q20. Quel réalisateur a travaillé avec le plus grand nombre d'acteurs distincts ?**")
st.write(f"Le réalisateur **{q20()['d.name']}**  a travaillé avec le plus grand nombre d'acteurs distincts : **{q20()['NombreActeurs']}** acteurs.")
st.write("---")

st.markdown("#### **Q21. Quels sont les films les plus “connectés”, c'est-à-dire ceux qui ont le plus d'acteurs en commun avec d'autres films ?**")
st.write(f"Les films les plus 'connectés', c'est-à-dire ceux qui ont le plus d'acteurs en commun avec d'autres films sont :")
st.write("\n".join([f"- **{film['f1.title']}** avec **{film['NombreFilmsConnectes']}** films connectés" for film in q21()]))
st.write("---")

st.markdown("#### **Q22. Trouver les 5 acteurs ayant joué avec le plus de réalisateurs différents.**")
st.write(f"Les 5 acteurs ayant joué avec le plus de réalisateurs différents sont :")
st.write("\n".join([f"- **{acteur['a.name']}** avec **{acteur['NombreRealisateurs']}** réalisateurs différents" for acteur in q22()]))
st.write("---")

st.markdown("#### **Q23. Recommander un film à un acteur en fonction des genres des films où il a déjà joué.**")
st.write(f"Films recommandés à un acteur (Chris Pratt) en fonction des genres des films où il a déjà joué :**{q23()['f2.title']}** ({q23()['f2.genre']})")
st.write("---")

st.markdown("#### **Q24. Créer une relation INFLUENCE PAR entre les réalisateurs en se basant sur des similarités dans les genres de films qu'ils ont réalisés.**")
st.write(f"Nombre de relations d'influence : **{q24_1()['count(r)']}**.")

st.write(f"Les réalisateurs influencés par Kenneth Lonergan sont :")
st.write("\n".join([f"- **{r['d1.name']}**" for r in q24_2()]))
st.write("---")

st.markdown("#### **Q25. Quel est le “chemin” le plus court entre deux acteurs donnés (ex : Tom Hanks et Scarlett Johansson) ?**")
# Initialisation des variables pour les acteurs et films
acteurs = []
films = []

# Parcourir les éléments du chemin pour extraire les acteurs et films
for element in q25()['p']:
    if 'name' in element:  # Si c'est un acteur
        acteurs.append(element['name'])
    elif 'title' in element:  # Si c'est un film
        films.append(element['title'])

# Créer une chaîne de caractères qui décrit le chemin
chemin_str = " → ".join([f"{acteurs[i]} → {films[i]} → {acteurs[i+1]}" for i in range(len(acteurs)-1)])
st.write(f"Le 'chemin' le plus court entre deux acteurs (Daniel Giménez Cacho et Scarlett Johansson) est : \n{chemin_str}")
st.write("---")

st.markdown("#### **Q26. Analyser les communautés d'acteurs : Quels sont les groupes d'acteurs qui ont tendance à travailler ensemble ? (Utilisation d'algorithmes de détection de communauté comme Louvain.)**")
#st.subheader("Communautés d'acteurs selon Louvain")
st.write("Toutes les communautés d'acteurs selon Louvain")
def q26():
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films)<-[:A_JOUE]-(b:Actors)
                           WHERE a <> b
                           RETURN a.name AS Actor1, b.name AS Actor2, COUNT(f) AS CommonFilms""")
    
    # Créer un DataFrame à partir des résultats
    data = pd.DataFrame(result)

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

    st.write("Chaque communauté d'acteurs selon Louvain")
    # Créer et afficher un graphe pour chaque communauté
    community_plots = []
    for community_id, actors in communities.items():
        # Sous-graphe pour cette communauté
        subgraph = G.subgraph(actors)
        
        # Créer une liste de couleurs pour les nœuds de ce sous-graphe
        node_colors = [partition[actor] for actor in subgraph.nodes()]
        pos = nx.spring_layout(subgraph)
        
        # Visualiser le sous-graphe
        fig, ax = plt.subplots(figsize=(4, 4))  
        nx.draw_networkx_nodes(subgraph, pos, node_size=30, cmap=plt.cm.jet, node_color=node_colors, ax=ax)
        nx.draw_networkx_edges(subgraph, pos, alpha=0.5, ax=ax)
        nx.draw_networkx_labels(subgraph, pos, font_size=5, ax=ax)
        ax.set_title(f"Communauté {community_id}", fontsize=10)
            
        # Sauvegarder l'image dans un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        community_plots.append(buf)
        
        plt.close(fig)

    cols = st.columns(2)
    # Afficher les graphiques des communautés dans Streamlit
    for idx, plot in enumerate(community_plots):
        with cols[idx % 2]:  # Alterner entre les colonnes
            st.image(plot, use_container_width=True)

# Exécution de q26
q26()

# Fermer la connexion Neo4j
conn.close()























