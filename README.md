## NoSQL Databases - Projet
Exploration et Interrogation de Bases de Données 

NoSQL avec Python

2024 - 2025


## Présentation du projet
Le but de ce projet est de nous familiariser avec deux types de systèmes de gestion de bases
de données NoSQL : MongoDB, une base de données orientée document, et Neo4j, une base
de données orientée graphe. J'ai développé une application en Python capable d’interagir
avec deux bases de données hébergées NOSQL dans le cloud, en répondant aux questions et en
récupérant les données pertinentes.


## Structure du projet
nosql_project/
│── connexion/               # Gestion des connexions aux bases de données et fonctions des requêtes
│   ├── bd_neo4j.py             # Importation des données de MongoDB à Neo4j
│   ├── mongo_co.py             # Connexion à MongoDB
│   ├── mongo_queries.py        # Requêtes pour MongoDB
│   ├── neo4j_co.py             # Connexion à Neo4j
│   ├── neo4j_queries.py        # Requêtes pour Neo4j
│   ├── transversale_queries.py # Requêtes combinant MongoDB et Neo4j
│── pages/               # Pages Streamlit
│── ├── mongo_page.py       # Configuration de l'affichage des réponses des requêtes MongoDB
│── ├── neo4j_page.py       # Configuration de l'affichage des réponses des requêtes Neo4j
│── ├── transversale_page.py       # Configuration de l'affichage des réponses des requêtes transversales (Neo4j)
│── app.py                      # Point d’entrée principal de l’application Streamlit
│── config.py                   # Fichier de configuration du projet
│── .env                        # Variables d’environnement (MongoDB, Neo4j)
│── .gitignore                  # Fichiers à ignorer dans Git
│── requirements.txt             # Liste des dépendances
│── docker-compose.yml           # Configuration Docker pour MongoDB et Neo4j
│── README.md                    # Documentation du projet


## Application
Le projet existe déjà en application déployée en ligne donc vous pouvez la trouver ici :
https://nosqlproject-zpvtshappqwgqz4jycuxvox.streamlit.app/

Si vous voulez lancer l'application vous-même, suivez les étapes des prérequis.

## Prérequis
- Récupérer le projet :
git clone https://github.com/SpirouSl6/nosql_project.git

- Installer les dépendances du projet :
pip install -r requirements.txt

- Vérifier que Streamlit est dans votre PATH, pour cela entrez streamlit à la racine du projet : streamlit 

Si Streamlit n'est pas reconnu, dans un terminal :
pip show streamlit

Récupérez la location et modifiez la fin du PATH pour avoir Python312\  (312 est ma version de python, vous pourriez en avoir une différente). Ajoutez ensuite ce chemin au PATH.

- Ajoutez le fichier .env à la racine du projet

- Pour lancer l'application, dans le terminal à la racine du projet : 
streamlit run app.py

## Bases de données utilisées
- MongoDB (avec MongoDB Atlas)
- Neo4j (avec Neo4j Aura)

## Auteur
Sarah Rialland Tardy