import mysql.connector
from mysql.connector import Error
import uuid
import os
from dotenv import load_dotenv
import random

import mysql.connector
from mysql.connector import Error
import uuid
import os
from dotenv import load_dotenv

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

if __name__ == "__main__":
    create_connection()

if __name__ == "__main__":
    create_connection()

def execute_query(connection, query, data):
    """Execute a single query"""
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")

def insert_bulk_data():
    connection = create_connection()

    if connection is None:
        return

    # Inserting approximately 500,000 rows into CUSTOMERS table
    customers_query = """
    INSERT INTO CUSTOMERS (CustomerID, FirstName, LastName, Email, Phone, Address)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    customers_data = [
        (str(uuid.uuid4()), f'FirstName{i}', f'LastName{i}', f'customer{i}@example.com', f'12345678{i}', f'Address {i}')
        for i in range(500000)
    ]
    for data in customers_data:
        execute_query(connection, customers_query, data)

    # Inserting approximately 500,000 rows into PRODUCTS table
    products_query = """
    INSERT INTO PRODUCTS (ProductID, ProductName, SKU, Price, StockQuantity)
    VALUES (%s, %s, %s, %s, %s)
    """
    products_data = [
        (str(uuid.uuid4()), f'Product{i}', f'SKU{i:06}', round(random.uniform(5.0, 500.0), 2), random.randint(1, 1000))
        for i in range(500000)
    ]
    for data in products_data:
        execute_query(connection, products_query, data)

    # Inserting approximately 500,000 rows into ORDERS table
    orders_query = """
    INSERT INTO ORDERS (OrderID, CustomerID, Status, TotalAmount)
    VALUES (%s, %s, %s, %s)
    """
    orders_data = [
        (str(uuid.uuid4()), customers_data[random.randint(0, 499999)][0], random.choice(['Pending', 'Shipped', 'Delivered']), round(random.uniform(20.0, 2000.0), 2))
        for _ in range(500000)
    ]
    for data in orders_data:
        execute_query(connection, orders_query, data)

    connection.close()

if __name__ == "__main__":
    insert_bulk_data()
