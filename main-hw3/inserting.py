import mysql.connector
from mysql.connector import Error
import uuid
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

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

# Existing functions ...

def insert_inventory(connection, product_ids):
    # Inserting data into INVENTORY table
    inventory_query = """
    INSERT INTO INVENTORY (InventoryID, ProductID, StockQuantity)
    VALUES (%s, %s, %s)
    """
    for product_id in product_ids:
        stock_quantity = random.randint(50, 500)  # Random stock quantity between 50 and 500
        data = (
            str(uuid.uuid4()),
            product_id,
            stock_quantity
        )
        execute_query(connection, inventory_query, data)

def insert_shipments(connection, order_ids):
    # Inserting data into SHIPMENTS table
    shipments_query = """
    INSERT INTO SHIPMENTS (ShipmentID, OrderID, ShipmentDate, Status)
    VALUES (%s, %s, %s, %s)
    """
    statuses = ['Processing', 'Shipped', 'Delivered']
    for order_id in order_ids:
        shipment_date = (datetime.now() - timedelta(days=random.randint(0, 10))).strftime('%Y-%m-%d')
        status = random.choice(statuses)
        data = (
            str(uuid.uuid4()),
            order_id,
            shipment_date,
            status
        )
        execute_query(connection, shipments_query, data)

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        # Insert products manually
        product_ids = insert_manual_data(connection)

        # Insert 500,000 customers
        insert_customers(connection, count=500000)

        # Fetch all customer IDs to use for orders
        cursor = connection.cursor()
        cursor.execute("SELECT CustomerID FROM CUSTOMERS")
        customer_ids = [row[0] for row in cursor.fetchall()]

        # Insert 500,000 orders
        insert_orders(connection, customer_ids, count=500000)

        # Fetch all order IDs to use for order items and shipments
        cursor.execute("SELECT OrderID FROM ORDERS")
        order_ids = [row[0] for row in cursor.fetchall()]

        # Insert 500,000 order items
        insert_order_items(connection, order_ids, product_ids, count=500000)

        # Insert inventory entries for products
        insert_inventory(connection, product_ids)

        # Insert shipments for orders
        insert_shipments(connection, order_ids)

        # Close connection
        connection.close()
