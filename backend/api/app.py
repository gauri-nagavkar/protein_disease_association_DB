from flask import Flask, request, jsonify
from backend.db.db_setup import create_db_connection, create_database
from backend.db.models import CREATE_PROTEIN_ASSOCIATIONS_TABLE, CREATE_AGGREGATE_ASSOCIATIONS_TABLE
from services.llm_service import analyze_paper

app = Flask(__name__)

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
    return "Protein Associations API is running!"

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

# Print all registered routes
print(app.url_map)

# Initialize the database when the app starts
if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
