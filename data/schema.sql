CREATE DATABASE IF NOT EXISTS EcommerceDB;

USE EcommerceDB;

-- Drop tables if they exist
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS vendor;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS customer;

-- Vendor table
CREATE TABLE vendor (
    vendor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    hotline VARCHAR(20),
    description TEXT
);

-- Customer table
CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    bio TEXT
);

-- Address table (removed customer_id foreign key)
CREATE TABLE address (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    street VARCHAR(255),
    zip_code VARCHAR(20),
    city VARCHAR(255)
);

-- Payment table
CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    card_number VARCHAR(20),
    cvv VARCHAR(4),
    expiration_date DATE,
);

-- Profile table
CREATE TABLE profile (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    primary_address_id INT,
    primary_payment_id INT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (primary_address_id) REFERENCES address(address_id),
    FOREIGN KEY (primary_payment_id) REFERENCES payment(payment_id)
);

-- Category table
CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Product table (without explicit constraint names)
CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INT DEFAULT 1,
    discount DECIMAL(5, 2) DEFAULT 1 CHECK (discount >= 0 AND discount <= 1),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

-- Orders table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    created_by INT,
    quantity INT DEFAULT 1,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    FOREIGN KEY (created_by) REFERENCES vendor(vendor_id)
);

