CREATE DATABASE orderManagement;
USE orderManagement;

CREATE TABLE customers(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
email VARCHAR(50) UNIQUE,
phone VARCHAR(15),
created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50)
);

CREATE TABLE products(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
description VARCHAR(999),
category_id INT,
price DOUBLE ,
stock_quantity INT,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (category_id) references categories(id)
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    status VARCHAR(50),
    total_amount DOUBLE,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items(
id INT PRIMARY KEY AUTO_INCREMENT,
order_id INT,
product_id INT,
quantity INT,
unit_price DOUBLE,
FOREIGN KEY (order_id) references orders(id),
FOREIGN KEY (product_id) references products(id)

);

CREATE TABLE users(
id INT PRIMARY KEY AUTO_INCREMENT,
username VARCHAR(50) UNIQUE,
password_hash VARCHAR(255),
role VARCHAR(20)
);

-- Categories
INSERT INTO categories (name) VALUES
('Electronics'), ('Stationery'), ('Furniture'), ('Kitchenware');

-- Customers (note: Sahil Singh will have NO orders - tests that query)
INSERT INTO customers (name, email, phone) VALUES
('Aman Sharma', 'amaan@example.com', '9876543210'),
('Priya Verma', 'priyaa@example.com', '9123456780'),
('Rohit Gupta', 'rohitt@example.com', '9988776655'),
('Sneha Patel', 'a@example.com', '9765432109'),
('Sahil Singh', 'sahill@example.com', '9012345678');

-- Products (note: 'USB Cable' and 'Stapler' have low stock - tests that query)
INSERT INTO products (name, description, category_id, price, stock_quantity) VALUES
('Wireless Mouse', 'Bluetooth mouse', 1, 599.00, 50),
('USB Cable', 'Type-C cable 1m', 1, 199.00, 5),
('Keyboard', 'Mechanical keyboard', 1, 2499.00, 30),
('Notebook', 'A5 ruled notebook', 2, 49.00, 200),
('Stapler', 'Standard office stapler', 2, 99.00, 8),
('Pen Set', 'Pack of 5 gel pens', 2, 79.00, 150),
('Office Chair', 'Ergonomic chair', 3, 4999.00, 15),
('Study Table', 'Wooden study table', 3, 3499.00, 10),
('Coffee Mug', 'Ceramic mug 350ml', 4, 149.00, 80),
('Lunch Box', 'Insulated steel lunch box', 4, 349.00, 40);

-- Orders (spanning 3 months: April, May, June 2025)
INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES
(1, '2025-04-05', 'delivered', 798.00),
(2, '2025-04-12', 'delivered', 2499.00),
(3, '2025-04-20', 'cancelled', 199.00),
(1, '2025-05-02', 'delivered', 4999.00),
(4, '2025-05-10', 'delivered', 296.00),
(2, '2025-05-18', 'pending', 99.00),
(3, '2025-06-01', 'delivered', 3848.00),
(1, '2025-06-08', 'delivered', 149.00),
(4, '2025-06-15', 'delivered', 698.00),
(2, '2025-06-20', 'shipped', 349.00);

-- Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
-- Order 1 (Aman, Apr) - Mouse + USB Cable
(1, 1, 1, 599.00),
(1, 2, 1, 199.00),
-- Order 2 (Priya, Apr) - Keyboard
(2, 3, 1, 2499.00),
-- Order 3 (Rohit, Apr, cancelled) - USB Cable
(3, 2, 1, 199.00),
-- Order 4 (Aman, May) - Office Chair
(4, 7, 1, 4999.00),
-- Order 5 (Sneha, May) - Notebook x2 + Pen Set
(5, 4, 2, 49.00),
(5, 6, 2, 79.00),
-- Order 6 (Priya, May, pending) - Stapler
(6, 5, 1, 99.00),
-- Order 7 (Rohit, June) - Study Table + Keyboard
(7, 8, 1, 3499.00),
(7, 3, 1, 2499.00) -- note: this exceeds total_amount, fine for test data realism isn't perfect
,
-- Order 8 (Aman, June) - Coffee Mug
(8, 9, 1, 149.00),
-- Order 9 (Sneha, June) - Mouse + Lunch Box
(9, 1, 1, 599.00),
(9, 10, 1, 349.00),
-- Order 10 (Priya, June, shipped) - Lunch Box
(10, 10, 1, 349.00);

-- Top 5 best-selling products (by quantity sold)
SELECT p.name, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY oi.product_id ,p.name
ORDER By total_Sold desc
LIMIT 5;

-- Customers who haven't ordered anything
SELECT c.id ,c.name 
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
-- ALTERNATE WAY
SELECT id, name FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);

-- Low stock products (e.g., stock_quantity < 10)
SELECT id, name, stock_quantity FROM products WHERE stock_quantity < 10;

-- Total revenue per category
SELECT c.name AS category , SUM(oi.quantity * unit_price) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.id
JOIN categories c ON p.category_id = c.id
GROUP BY c.id, c.name
ORDER BY total_revenue DESC;

-- Monthly revenue trend
SELECT DATE_FORMAT(order_date, '%y-%m') AS month, SUM(total_amount) AS revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%y-%m')
ORDER BY month;





