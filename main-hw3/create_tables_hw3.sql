CREATE DATABASE ecommerce_shop;
USE ecommerce_shop;

-- CUSTOMERS table stores customer information
CREATE TABLE CUSTOMERS (
    CustomerID VARCHAR(36) PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Email VARCHAR(200) UNIQUE NOT NULL,
    Phone VARCHAR(20),
    Address VARCHAR(255),
    DateCreated DATETIME DEFAULT CURRENT_TIMESTAMP
) COMMENT='Table storing customer information for the e-commerce shop';

-- PRODUCTS table stores product information
CREATE TABLE PRODUCTS (
    ProductID VARCHAR(36) PRIMARY KEY,
    ProductName VARCHAR(200) NOT NULL,
    SKU VARCHAR(50) UNIQUE NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    StockQuantity INT NOT NULL,
    DateAdded DATETIME DEFAULT CURRENT_TIMESTAMP
) COMMENT='Table storing product details for the e-commerce shop';

-- ORDERS table stores customer order information
CREATE TABLE ORDERS (
    OrderID VARCHAR(36) PRIMARY KEY,
    CustomerID VARCHAR(36),
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(50) NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES CUSTOMERS(CustomerID)
) COMMENT='Table storing customer orders';

-- ORDER_ITEMS table represents the relationship between orders and products
CREATE TABLE ORDER_ITEMS (
    OrderItemID VARCHAR(36) PRIMARY KEY,
    OrderID VARCHAR(36),
    ProductID VARCHAR(36),
    Quantity INT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES ORDERS(OrderID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCTS(ProductID)
) COMMENT='Table storing items within an order, representing order-product relationships';

-- INVENTORY table tracks stock levels for each product
CREATE TABLE INVENTORY (
    InventoryID VARCHAR(36) PRIMARY KEY,
    ProductID VARCHAR(36),
    StockQuantity INT NOT NULL,
    LastUpdated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ProductID) REFERENCES PRODUCTS(ProductID)
) COMMENT='Table tracking inventory for each product';

-- SHIPMENTS table stores shipping details related to orders
CREATE TABLE SHIPMENTS (
    ShipmentID VARCHAR(36) PRIMARY KEY,
    OrderID VARCHAR(36),
    ShipmentDate DATETIME,
    DeliveryDate DATETIME,
    Status VARCHAR(50),
    FOREIGN KEY (OrderID) REFERENCES ORDERS(OrderID)
) COMMENT='Table storing shipment details for orders';


-- Add additional constraints for data integrity
-- Removing duplicate constraint
-- ALTER TABLE PRODUCTS ADD CONSTRAINT chk_price CHECK (Price > 0);

-- Add additional constraints for data integrity
ALTER TABLE PRODUCTS ADD CONSTRAINT chk_price CHECK (Price > 0);

ALTER TABLE ORDER_ITEMS
ADD CONSTRAINT chk_quantity CHECK (Quantity > 0);

-- Add comments to tables and columns
ALTER TABLE CUSTOMERS COMMENT = 'This table stores customer data, including contact information and address';
ALTER TABLE CUSTOMERS MODIFY COLUMN Email VARCHAR(200) COMMENT 'Customer email, must be unique';

ALTER TABLE PRODUCTS COMMENT = 'Table storing details of products available in the shop';
ALTER TABLE PRODUCTS MODIFY COLUMN SKU VARCHAR(50) COMMENT 'Unique Stock Keeping Unit identifier for each product';

ALTER TABLE ORDERS COMMENT = 'This table stores information about customer orders';
ALTER TABLE ORDERS MODIFY COLUMN Status VARCHAR(50) COMMENT 'Order status (e.g., Pending, Shipped, Delivered)';



