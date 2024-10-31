USE ecommerce_shop;

-- Create user and grant privileges
CREATE USER 'ecom_user'@'localhost' IDENTIFIED BY 'fifadg13';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_shop.* TO 'ecom_user'@'localhost';
FLUSH PRIVILEGES;


ALTER USER 'ecom_user'@'localhost' IDENTIFIED BY 'fifadg13';
FLUSH PRIVILEGES;

