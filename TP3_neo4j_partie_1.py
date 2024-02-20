# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:25:10 2024

@author: Hp
"""

# Importation du driver Neo4j pour Python
from neo4j import GraphDatabase

# informations d'identification de la base de données
uri = "bolt://localhost:7687"
userName = "neo4j"
password = "neo4j"

# Connect to the Neo4j database server
graphDB_Driver = GraphDatabase.driver(uri, auth=(userName, password))

# CQL pour interroger toutes les universités présentes dans le graphe
cqlNodeQuery = "MATCH (x:university) RETURN x"

# CQL pour interroger les distances de Yale vers certaines autres universités Ivy League
cqlEdgeQuery = "MATCH (x:university {name:'Yale University'})-[r]->(y:university) RETURN y.name,r.miles"

# CQL pour créer un graphe contenant certaines des universités Ivy League
cqlCreate = """CREATE (cornell:university { name: "Cornell University"}),
(yale:university { name: "Yale University"}),
(princeton:university { name: "Princeton University"}),
(harvard:university { name: "Harvard University"}), 
(cornell)-[:connects_in {miles: 259}]->(yale),
(cornell)-[:connects_in {miles: 210}]->(princeton),
(cornell)-[:connects_in {miles: 327}]->(harvard),
(yale)-[:connects_in {miles: 259}]->(cornell),
(yale)-[:connects_in {miles: 133}]->(princeton),
(yale)-[:connects_in {miles: 133}]->(harvard),
(harvard)-[:connects_in {miles: 327}]->(cornell),
(harvard)-[:connects_in {miles: 133}]->(yale),
(harvard)-[:connects_in {miles: 260}]->(princeton),
(princeton)-[:connects_in {miles: 210}]->(cornell),
(princeton)-[:connects_in {miles: 133}]->(yale),
(princeton)-[:connects_in {miles: 260}]->(harvard)"""

# CQL pour ajouter un nouveau nœud pour Brown University
cqlAjouterBrown = "CREATE (brown:university { name: 'Brown University'})"

# CQL pour ajouter des relations entre Brown University et les autres universités Ivy League
cqlAjouterRelationsBrown = """
MATCH (brown:university { name: 'Brown University' }),
      (cornell:university { name: 'Cornell University' }),
      (yale:university { name: 'Yale University' }),
      (princeton:university { name: 'Princeton University' }),
      (harvard:university { name: 'Harvard University' })
CREATE (brown)-[:connects_in {miles: 150}]->(cornell),
      (brown)-[:connects_in {miles: 100}]->(yale),
      (brown)-[:connects_in {miles: 120}]->(princeton),
      (brown)-[:connects_in {miles: 50}]->(harvard)
"""
# Execute the CQL query
with graphDB_Driver.session() as graphDB_Session:
    # Create nodes
    graphDB_Session.run(cqlCreate)
# Query the graph    
    nodes = graphDB_Session.run(cqlNodeQuery) 
    print("List of Ivy League universities present in the graph:")
    for node in nodes:
        print(node)
    # Query the relationships present in the graph
    nodes = graphDB_Session.run(cqlEdgeQuery)
    print("Distance from Yale University to the other Ivy League universities present in the graph:")
    for node in nodes:
        print(node)
    # Création du nœud pour Brown University
    graphDB_Session.run(cqlAjouterBrown)
    print("Brown University a été ajoutée au graphe.")
    
    # Ajout des relations pour Brown University
    graphDB_Session.run(cqlAjouterRelationsBrown)
    print("Les relations pour Brown University ont été ajoutées au graphe.")   