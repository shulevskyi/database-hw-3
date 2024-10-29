import mysql.connector
from mysql.connector import Error
import uuid
import os
from dotenv import load_dotenv
import random

# Load environment variables from .env file
load_dotenv(override=True)  # This forces loading from .env, overriding existing system environment variables

# Connection settings (read from .env file)
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

# Debugging to check loaded environment variables
print(f"HOST: {HOST}")
print(f"USER: {USER}")
print(f"PASSWORD: {PASSWORD}")
print(f"DATABASE: {DATABASE}")

def create_connection():
    """Create a database connection"""
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, query, data):
    """Execute a single query"""
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def insert_customers(connection, count=1000):
    # Inserting data into CUSTOMERS table
    customers_query = """
    INSERT INTO CUSTOMERS (CustomerID, FirstName, LastName, Email, Phone, Address)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for i in range(count):
        email = f"customer_{random.randint(100000, 999999)}@example.com"
        data = (
            str(uuid.uuid4()),
            f'CustomerFirstName{i}',
            f'CustomerLastName{i}',
            email,
            f'123456789{i}',
            f'Address {i}, City, Country'
        )
        execute_query(connection, customers_query, data)

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        insert_customers(connection, count=500000)
        connection.close()