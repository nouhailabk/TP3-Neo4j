# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 17:43:15 2024

@author: Hp
"""

from neo4j import GraphDatabase

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "neo4j"  

driver = GraphDatabase.driver(uri, auth=(username, password))

def import_data(tx, max_lines):
    # Importation limitée des régions
    tx.run(f"""
        LOAD CSV WITH HEADERS FROM 'file:///communes-departement-region.csv' AS line
        WITH line LIMIT {max_lines}
        MERGE (region:Region {{code: line.code_region, name: line.nom_region}});
    """)
    
    # Importation limitée des départements
    tx.run(f"""
        LOAD CSV WITH HEADERS FROM 'file:///communes-departement-region.csv' AS line
        WITH line LIMIT {max_lines}
        MERGE (department:Department {{code: line.code_departement, name: line.nom_departement}})
        WITH department, line
        MATCH (region:Region {{code: line.code_region}})
        MERGE (department)-[:BELONGS_TO]->(region);
    """)
    
    # Importation limitée des communes
    tx.run(f"""
        LOAD CSV WITH HEADERS FROM 'file:///communes-departement-region.csv' AS line
        WITH line LIMIT {max_lines}
        MERGE (commune:Commune {{
            code_INSEE: line.code_commune_INSEE,
            name: line.nom_commune,
            postal_code: line.code_postal,
            latitude: toFloat(line.latitude),
            longitude: toFloat(line.longitude)
        }})
        WITH commune, line
        MATCH (department:Department {{code: line.code_departement}})
        MERGE (commune)-[:BELONGS_TO]->(department);
    """)
def add_mayors(tx):
    # Liste des maires à ajouter (remplacez par vos données)
    maires = [
        {"code_INSEE": "75056", "nom": "Anne Hidalgo", "mandat_debut": 2014},
        {"code_INSEE": "13055", "nom": "Benoit Payan", "mandat_debut": 2022},
        # Ajoutez d'autres maires ici
    ]
    for maire in maires:
        tx.run("""
            MATCH (commune:Commune {code_INSEE: $code_INSEE})
            MERGE (maire:Maire {nom: $nom})
            ON CREATE SET maire.mandat_debut = $mandat_debut
            MERGE (maire)-[:EST_MAIRE_DE]->(commune)
        """, code_INSEE=maire["code_INSEE"], nom=maire["nom"], mandat_debut=maire["mandat_debut"])

max_import_lines = 10000  # Modifier ce nombre pour contrôler le nombre total de lignes importées

# Exécution des transactions pour l'importation
with driver.session() as session:
    session.write_transaction(import_data, max_import_lines)
    session.write_transaction(add_mayors)

driver.close()  # Fermeture de la connexion








