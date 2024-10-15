# This file contains the SQL queries for creating and managing tables in the database

# Table to store individual protein-disease association records
CREATE_PROTEIN_ASSOCIATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS ProteinAssociations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    protein_name VARCHAR(255) NOT NULL,
    disease_name VARCHAR(255) NOT NULL,
    association_type ENUM('Positive', 'Negative', 'Neutral') NOT NULL,
    publication VARCHAR(255),
    citation_count INT,
    author_list TEXT,
    publication_date DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""

# Table to store aggregated data for protein-disease associations
CREATE_AGGREGATE_ASSOCIATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS AggregateAssociations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    protein_name VARCHAR(255) NOT NULL,
    disease_name VARCHAR(255) NOT NULL,
    strong_association ENUM('Strong Association', 'Strong Disassociation', 'None') DEFAULT 'None',
    total_citations INT,
    total_publications INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""
