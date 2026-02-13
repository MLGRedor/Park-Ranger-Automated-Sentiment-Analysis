import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load the secure credentials from the .env file
load_dotenv()

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD").strip(),
            database=os.getenv("DB_NAME"),
            port=3307,
            auth_plugin='mysql_native_password' 
        )
        if connection.is_connected():
            print("Success! Connected to the Park Ranger MySQL Database.")
            return connection
            
    except Error as e:
        print(f"Error: '{e}' occurred while connecting to MySQL.")
        return None

if __name__ == "__main__":
    conn = create_db_connection()
    if conn:
        conn.close()
        print("Test complete. Connection securely closed.")