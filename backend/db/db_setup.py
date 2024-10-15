import mysql.connector
from backend.utils.config import DB_CONFIG

# Function to create the MySQL database if it doesn't exist
def create_database():
    try:
        # Connect without specifying a database
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        # Check if the database exists, if not, create it
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']};")
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")

# Function to create a connection to the MySQL database
def create_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
