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

-- Indexes
CREATE INDEX idx_email ON CUSTOMERS (Email);
CREATE INDEX idx_customer_id ON ORDERS (CustomerID);
CREATE INDEX idx_order_id ON ORDER_ITEMS (OrderID);
CREATE INDEX idx_product_id ON ORDER_ITEMS (ProductID);
CREATE INDEX idx_inventory_product_id ON INVENTORY (ProductID);
CREATE INDEX idx_shipment_order_id ON SHIPMENTS (OrderID);

-- Indexes optimization check
SET profiling = 1;
SELECT * FROM CUSTOMERS IGNORE INDEX (idx_email) WHERE Email = 'customer_00003b5cc897454d86359d4420288e53@example.com';
SELECT * FROM ORDERS IGNORE INDEX (idx_customer_id) WHERE CustomerID = '00005167-25ff-49fb-a3b0-682234ade0f9';
SELECT * FROM ORDER_ITEMS IGNORE INDEX (idx_order_id) WHERE OrderID = '000023d4-bda7-40d4-a43a-a460e27088e2';
SELECT * FROM INVENTORY IGNORE INDEX (idx_inventory_product_id) WHERE ProductID = '000023d4-bda7-40d4-a43a-a460e27088e2';
SHOW PROFILES;
SET profiling = 0;
SET profiling = 1;
SELECT * FROM CUSTOMERS WHERE Email = 'customer_00003b5cc897454d86359d4420288e53@example.com';
SELECT * FROM ORDERS WHERE CustomerID = '00005167-25ff-49fb-a3b0-682234ade0f9';
SELECT * FROM ORDER_ITEMS WHERE OrderID = '000023d4-bda7-40d4-a43a-a460e27088e2';
SELECT * FROM INVENTORY WHERE ProductID = '000023d4-bda7-40d4-a43a-a460e27088e2';
SHOW PROFILES;
SET profiling = 0;


CREATE VIEW top_products AS
SELECT
    p.ProductID,
    p.ProductName,
    SUM(oi.Quantity) AS TotalSales
FROM PRODUCTS p
JOIN ORDER_ITEMS oi ON p.ProductID = oi.ProductID
JOIN ORDERS o ON oi.OrderID = o.OrderID
WHERE MONTH(o.OrderDate) = MONTH(CURRENT_DATE()) AND YEAR(o.OrderDate) = YEAR(CURRENT_DATE())
GROUP BY p.ProductID
ORDER BY TotalSales DESC
