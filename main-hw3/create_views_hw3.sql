USE ecommerce_shop;

-- Create a view that shows customer orders
CREATE VIEW customer_orders AS
SELECT CUSTOMERS.CustomerID, CUSTOMERS.FirstName, CUSTOMERS.LastName, ORDERS.OrderID, ORDERS.TotalAmount
FROM CUSTOMERS
JOIN ORDERS ON CUSTOMERS.CustomerID = ORDERS.CustomerID;

-- Create a view that shows order details with products
CREATE VIEW order_details AS
SELECT ORDERS.OrderID, PRODUCTS.ProductName, ORDER_ITEMS.Quantity, ORDER_ITEMS.Price
FROM ORDERS
JOIN ORDER_ITEMS ON ORDERS.OrderID = ORDER_ITEMS.OrderID
JOIN PRODUCTS ON ORDER_ITEMS.ProductID = PRODUCTS.ProductID;
