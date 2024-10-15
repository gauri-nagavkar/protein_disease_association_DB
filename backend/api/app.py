from flask import Flask
from backend.db.db_setup import create_db_connection, create_database
from backend.db.models import CREATE_PROTEIN_ASSOCIATIONS_TABLE, CREATE_AGGREGATE_ASSOCIATIONS_TABLE

app = Flask(__name__)

# Test MySQL connection
def test_mysql_connection():
    connection = create_db_connection()
    if connection:
        print("Successfully connected to MySQL!")
        connection.close()
    else:
        print("Failed to connect to MySQL.")

# Initialize the database (create it if it doesn't exist) and create tables
def initialize_db():
    test_mysql_connection 
    # First, create the database if it doesn't exist
    create_database()

    # Now connect to the newly created or existing database and set up tables
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        # Create tables if they don't exist
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

# Initialize the database when the app starts
if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)