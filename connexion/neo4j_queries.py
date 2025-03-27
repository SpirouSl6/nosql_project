from neo4j_co import Neo4jConnection
import networkx as nx
import community as community_louvain
import pandas as pd
import matplotlib.pyplot as plt

# Récupérer et afficher les films dans Neo4j
conn = Neo4jConnection()

def q14():
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films) 
                        RETURN a.name, COUNT(f) AS FilmCount 
                        ORDER BY FilmCount DESC 
                        LIMIT 1""") 
    return result

def q15():
    result = conn.query(""""MATCH (a:Actors)-[:A_JOUE]->(f:Films)<-[:A_JOUE]-(ah:Actors {name: 'Anne Hathaway'}) 
                        RETURN a.name""") 
    return result

def q16_1():
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films) 
                        RETURN a.name, f.revenue AS TotalRevenue 
                        ORDER BY TotalRevenue DESC 
                        LIMIT 1""") 
    return result

def q16_2():
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films) 
                        WITH a, SUM(COALESCE(toFloat(f.revenue), 0)) AS TotalRevenue 
                        RETURN a.name, TotalRevenue 
                        ORDER BY TotalRevenue DESC 
                        LIMIT 1""") 
    return result

def q17():
    result = conn.query("""MATCH (f:Films) 
                        RETURN AVG(f.votes)""") 
    return result

def q18():
    result = conn.query("""MATCH (f:Films) 
                        UNWIND split(f.genre, ',') AS genre 
                        RETURN genre, COUNT(*) AS genre_count 
                        ORDER BY genre_count DESC 
                        LIMIT 1""") 
    return result

def q19():
    result = conn.query("""MATCH (a:Actors {name: 'Sarah Rialland Tardy'})-[:A_JOUE]->(f:Films)<-[:A_JOUE]-(other:Actors)-[:A_JOUE]->(fo:Films) 
                        WHERE other.name <> a 
                        RETURN fo.title""") 
    return result

def q20():
    result = conn.query("""MATCH (d:Realisateur)-[:A_REALISE]->(f:Films)<-[:A_JOUE]-(a:Actors)
                        RETURN d.name, COUNT(DISTINCT a) AS NombreActeurs
                        ORDER BY NombreActeurs DESC
                        LIMIT 1;""") 
    return result

def q21():
    result = conn.query("""MATCH (f1:Films)<-[:A_JOUE]-(a:Actors)-[:A_JOUE]->(f2:Films)
                        WHERE f1 <> f2
                        WITH f1, COUNT(DISTINCT f2) AS NombreFilmsConnectes
                        RETURN f1.title, NombreFilmsConnectes
                        ORDER BY NombreFilmsConnectes DESC
                        LIMIT 5;""") 
    return result

def q22():
    result = conn.query("""MATCH (a:Actors)-[:A_JOUE]->(f:Films)<-[:A_REALISE]-(d:Realisateur)
                        RETURN a.name, COUNT(DISTINCT d) AS NombreRealisateurs
                        ORDER BY NombreRealisateurs DESC
                        LIMIT 5;""") 
    return result

def q23():
    result = conn.query("""MATCH (a:Actors {name: "Chris Pratt"})-[:A_JOUE]->(f:Films)
                        UNWIND split(f.genre, ',') AS genre 
                        WITH a, collect(DISTINCT genre) AS genres_pref
                        MATCH (f2:Films)
                        WHERE ANY(genre IN genres_pref WHERE genre IN f2.genre)
                        AND NOT EXISTS { MATCH (a)-[:A_JOUE]->(f2) }  
                        RETURN f2.title, f2.genre
                        LIMIT 1;""") 
    return result

def q24_1():
    result = conn.query("""MATCH ()-[r:INFLUENCE_PAR]->()
                        RETURN count(r);""") 
    return result

def q24_2():
    result = conn.query("""MATCH (d1:Realisateur)-[:INFLUENCE_PAR]->(d2:Realisateur {name: "Kenneth Lonergan"})
                        RETURN d1.name;""") 
    return result


def q25():
    result = conn.query("""MATCH p = shortestPath((a1:Actors {name: "Daniel Giménez Cacho"})-[*..10]-(a2:Actors {name: "Scarlett Johansson"}))
                        RETURN p;""") 
    return result


# Fermer la connexion
conn.close()