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

def insert_manual_data(connection):
    # Manually inserting data into PRODUCTS table
    products_query = """
    INSERT INTO PRODUCTS (ProductID, ProductName, SKU, Price, StockQuantity)
    VALUES (%s, %s, %s, %s, %s)
    """
    products_data = [
        (str(uuid.uuid4()), 'Product A', 'SKU001', 19.99, 100),
        (str(uuid.uuid4()), 'Product B', 'SKU002', 29.99, 150),
        (str(uuid.uuid4()), 'Product C', 'SKU003', 39.99, 200)
    ]
    product_ids = []
    for data in products_data:
        execute_query(connection, products_query, data)
        product_ids.append(data[0])

    return product_ids

def insert_customers(connection, count=500000):
    # Inserting data into CUSTOMERS table
    customers_query = """
    INSERT INTO CUSTOMERS (CustomerID, FirstName, LastName, Email, Phone, Address)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for i in range(count):
        email = f"customer_{uuid.uuid4().hex}@example.com"  # Using UUID to ensure uniqueness
        data = (
            str(uuid.uuid4()),
            f'CustomerFirstName{i}',
            f'CustomerLastName{i}',
            email,
            f'123456789{i}',
            f'Address {i}, City, Country'
        )
        execute_query(connection, customers_query, data)

def insert_orders(connection, customer_ids, count=500000):
    # Inserting data into ORDERS table
    orders_query = """
    INSERT INTO ORDERS (OrderID, CustomerID, Status, TotalAmount)
    VALUES (%s, %s, %s, %s)
    """
    statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled']

    for i in range(count):
        customer_id = random.choice(customer_ids)  # Randomly select a customer ID for each order
        status = random.choice(statuses)
        total_amount = round(random.uniform(10.0, 500.0), 2)  # Random total amount between $10 and $500
        data = (
            str(uuid.uuid4()),
            customer_id,
            status,
            total_amount
        )
        execute_query(connection, orders_query, data)

def insert_order_items(connection, order_ids, product_ids, count=500000):
    # Inserting data into ORDER_ITEMS table
    order_items_query = """
    INSERT INTO ORDER_ITEMS (OrderItemID, OrderID, ProductID, Quantity, Price)
    VALUES (%s, %s, %s, %s, %s)
    """
    for i in range(count):
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 10)  # Random quantity between 1 and 10
        price = round(random.uniform(5.0, 100.0), 2)  # Random price between $5 and $100
        data = (
            str(uuid.uuid4()),
            order_id,
            product_id,
            quantity,
            price
        )
        execute_query(connection, order_items_query, data)

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
