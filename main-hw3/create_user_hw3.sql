USE ecommerce_shop;

-- Create user and grant privileges
CREATE USER 'ecom_user'@'localhost' IDENTIFIED BY 'fifadg13';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_shop.* TO 'ecom_user'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'data_analyst'@'localhost' IDENTIFIED BY 'analyst_password123';
GRANT SELECT ON ecommerce_shop.* TO 'data_analyst'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'data_entry'@'localhost' IDENTIFIED BY 'entry_password456';
GRANT SELECT, INSERT, UPDATE ON ecommerce_shop.* TO 'data_entry'@'localhost';
FLUSH PRIVILEGES;

