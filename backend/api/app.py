from flask import Flask, render_template, request, jsonify
from backend.db.db_setup import create_db_connection, create_database
from backend.db.models import CREATE_PROTEIN_ASSOCIATIONS_TABLE, CREATE_AGGREGATE_ASSOCIATIONS_TABLE
from services.llm_service import analyze_paper

import os

# Define the absolute paths for templates and static folders
template_dir = os.path.abspath("./templates")
static_dir = os.path.abspath("./static")

# Initialize the Flask app with the defined template and static directories
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# app = Flask(__name__)

# Initialize the database and create tables
def initialize_db():
    create_database()
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_PROTEIN_ASSOCIATIONS_TABLE)
        cursor.execute(CREATE_AGGREGATE_ASSOCIATIONS_TABLE)
        connection.commit()
        cursor.close()
        connection.close()
    else:
        print("Failed to connect to database.")

@app.route("/")
def index():
    return render_template("index.html")

# Route to insert new protein association record
@app.route("/add_association", methods=["POST"])
def add_association():
    data = request.json
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO ProteinAssociations 
            (protein_name, disease_name, association_type, publication, citation_count, author_list, publication_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data["protein_name"], data["disease_name"], data["association_type"],
            data["publication"], data["citation_count"], data["author_list"], data["publication_date"]
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Association added successfully"}), 201
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to retrieve all protein-disease associations
@app.route("/get_associations", methods=["GET"])
def get_associations():
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ProteinAssociations")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(records), 200
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to retrieve associations filtered by protein name
@app.route("/get_associations_by_protein/<protein_name>", methods=["GET"])
def get_associations_by_protein(protein_name):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM ProteinAssociations WHERE protein_name = %s"
        cursor.execute(query, (protein_name,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(records), 200
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to retrieve associations filtered by disease name
@app.route("/get_associations_by_disease/<disease_name>", methods=["GET"])
def get_associations_by_disease(disease_name):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM ProteinAssociations WHERE disease_name = %s"
        cursor.execute(query, (disease_name,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(records), 200
    else:
        return jsonify({"error": "Failed to connect to database"}), 500
    

# Route to analyze research papers and extract protein-disease associations
@app.route("/analyze_paper", methods=["POST"])
def analyze_paper_route():
    data = request.json

    # The request must contain the text of the research paper
    paper_text = data.get("paper_text")
    if not paper_text:
        return jsonify({"error": "Missing paper text"}), 400

    # Analyze the paper with the LLM
    result = analyze_paper(paper_text)

    if result:
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()

            # Insert each protein-disease association into the database
            for association in result:
                insert_query = """
                    INSERT INTO ProteinAssociations 
                    (protein_name, disease_name, association_type, publication, citation_count, author_list, publication_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    association['protein'], association['disease'], association['association'],
                    data.get("publication"), data.get("citation_count"),
                    data.get("author_list"), data.get("publication_date")
                ))

            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Paper analyzed and data inserted successfully"}), 201
        else:
            return jsonify({"error": "Database connection failed"}), 500
    else:
        return jsonify({"error": "Failed to analyze paper"}), 500

# Query associations by protein name
@app.route("/query_by_protein/<protein_name>", methods=["GET"])
def query_by_protein(protein_name):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM ProteinAssociations WHERE protein_name = %s"
        cursor.execute(query, (protein_name,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(records), 200
    else:
        return jsonify({"error": "Database connection failed"}), 500

# Query associations by disease name
@app.route("/query_by_disease/<disease_name>", methods=["GET"])
def query_by_disease(disease_name):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM ProteinAssociations WHERE disease_name = %s"
        cursor.execute(query, (disease_name,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(records), 200
    else:
        return jsonify({"error": "Database connection failed"}), 500

# Query associations by association type (Positive, Negative, or Neutral)
@app.route("/query_by_association/<association_type>", methods=["GET"])
def query_by_association(association_type):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM ProteinAssociations WHERE association_type = %s"
        cursor.execute(query, (association_type,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(records), 200
    else:
        return jsonify({"error": "Database connection failed"}), 500

# Query with multiple filters (Protein, Disease, and Association)
@app.route("/query_with_filters", methods=["GET"])
def query_with_filters():
    protein_name = request.args.get("protein_name")
    disease_name = request.args.get("disease_name")
    association_type = request.args.get("association_type")
    
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM ProteinAssociations WHERE 1=1"
        
        # Add conditions based on provided filters
        if protein_name:
            query += " AND protein_name = %s"
        if disease_name:
            query += " AND disease_name = %s"
        if association_type:
            query += " AND association_type = %s"
        
        params = [p for p in (protein_name, disease_name, association_type) if p]
        cursor.execute(query, params)
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(records), 200
    else:
        return jsonify({"error": "Database connection failed"}), 500
    
# Route to handle search requests
@app.route("/search", methods=["GET"])
def search():
    protein_name = request.args.get("protein_name")
    disease_name = request.args.get("disease_name")
    association_type = request.args.get("association_type")
    
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM ProteinAssociations WHERE 1=1"
        
        # Add conditions based on provided filters
        params = []
        if protein_name:
            query += " AND protein_name = %s"
            params.append(protein_name)
        if disease_name:
            query += " AND disease_name = %s"
            params.append(disease_name)
        if association_type:
            query += " AND association_type = %s"
            params.append(association_type)
        
        cursor.execute(query, params)
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Render results.html with the records
        return render_template("results.html", results=records)
    else:
        return jsonify({"error": "Database connection failed"}), 500

# Print all registered routes
print(app.url_map)

# Initialize the database when the app starts
if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
