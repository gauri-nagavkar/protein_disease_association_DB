from flask import request, jsonify
from db.db_setup import create_db_connection

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
