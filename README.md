# E-Commerce Database Management System

A Streamlit-based web application that provides a user-friendly interface for managing an e-commerce database system. This application allows users to interact with various aspects of the e-commerce platform, from customer management to product tracking and vendor analytics.

## Features

### Customer Management
- View customer profile information including contact details and addresses
- Track customer payment methods and preferences
- View customer order history

### Product Management
- Search products by name or description
- View products by categories
- Track product inventory and discounts
- Add new products to the database
- View popular products based on order history

### Vendor Operations
- Generate vendor sales reports
- View vendor information and performance metrics
- Track vendor-specific order statistics

### Order Processing
- View detailed order information
- Track products within specific orders
- Monitor order quantities and status

## Available Queries

1. **Find Customer Orders**: View all orders placed by a specific customer
2. **List Products in Order**: Display products and quantities in a specific order
3. **Vendor Sales Report**: Generate sales statistics for specific vendors
4. **Customer Profile Info**: View detailed customer information including address and payment details
5. **Product Categories**: Browse products by category
6. **Customer Payment Methods**: View customer payment information
7. **Product Search**: Search products by name or description
8. **Vendor Information**: View vendor details and performance metrics
9. **Popular Products**: View top products based on order frequency
10. **Product Discounts**: Browse products with active discounts
11. **Insert New Product**: Add new products to the database

## Example Queries

Here are some example SQL queries that demonstrate the capabilities of the system:

### 1. Find Customer Orders
Retrieves all orders placed by a specific customer, including order details and associated products.
```sql
SELECT o.order_id, 
       c.name AS customer_name,
       p.name AS product_name,
       o.quantity,
       v.name AS vendor_name
FROM orders o
JOIN customer c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
JOIN vendor v ON o.created_by = v.vendor_id
WHERE o.customer_id = [customer_id];
```

### 2. List Products in Order
Shows all products and their details for a specific order.
```sql
SELECT o.order_id,
       p.product_id,
       p.name AS product_name,
       p.description,
       o.quantity,
       p.discount,
       cat.name AS category_name
FROM orders o
JOIN product p ON o.product_id = p.product_id
LEFT JOIN category cat ON p.category_id = cat.category_id
WHERE o.order_id = [order_id];
```

### 3. Vendor Sales Report
Calculates total sales statistics for each vendor, including order counts and customer metrics.
```sql
SELECT v.vendor_id,
       v.name AS vendor_name,
       COUNT(DISTINCT o.order_id) AS total_orders,
       SUM(o.quantity) AS total_items_sold,
       COUNT(DISTINCT o.customer_id) AS unique_customers
FROM vendor v
LEFT JOIN orders o ON v.vendor_id = o.created_by
GROUP BY v.vendor_id, v.name;
```

### 4. Products by Category
Lists all products within a specific category with their details.
```sql
SELECT p.product_id,
       p.name AS product_name,
       p.description,
       p.quantity AS stock,
       p.discount,
       c.name AS category_name
FROM product p
JOIN category c ON p.category_id = c.category_id
WHERE c.category_id = [category_id];
```

### 5. Customer Payment Methods
Shows payment methods associated with customers and identifies primary payment methods.
```sql
SELECT DISTINCT c.customer_id,
       c.name AS customer_name,
       c.email,
       p.card_number,
       p.expiration_date,
       CASE WHEN pr.primary_payment_id = p.payment_id THEN 'Primary' ELSE 'Secondary' END AS payment_status
FROM customer c
JOIN profile pr ON c.customer_id = pr.customer_id
JOIN payment p ON pr.primary_payment_id = p.payment_id;
```

### 6. Vendor Order Statistics
Displays the total number of orders and unique customers for each vendor.
```sql
SELECT v.vendor_id,
       v.name AS vendor_name,
       COUNT(o.order_id) AS total_orders,
       COUNT(DISTINCT o.customer_id) AS unique_customers
FROM vendor v
LEFT JOIN orders o ON v.vendor_id = o.created_by
GROUP BY v.vendor_id, v.name;
```

### 7. Vendors Selling Specific Product
Identifies all vendors who have sold a particular product.
```sql
SELECT DISTINCT v.vendor_id,
       v.name AS vendor_name,
       v.hotline,
       p.name AS product_name,
       p.description
FROM vendor v
JOIN orders o ON v.vendor_id = o.created_by
JOIN product p ON o.product_id = p.product_id
WHERE p.product_id = [product_id];
```

### 8. Popular Products
Ranks products by order frequency and total quantity sold.
```sql
SELECT p.product_id,
       p.name AS product_name,
       COUNT(o.order_id) AS times_ordered,
       SUM(o.quantity) AS total_quantity_sold,
       cat.name AS category_name
FROM product p
LEFT JOIN orders o ON p.product_id = o.product_id
LEFT JOIN category cat ON p.category_id = cat.category_id
GROUP BY p.product_id, p.name, cat.name
ORDER BY times_ordered DESC, total_quantity_sold DESC
LIMIT 10;
```

### 9. Average Discount by Vendor
Calculates the average discount offered by each vendor across their products.
```sql
SELECT v.vendor_id,
       v.name AS vendor_name,
       AVG(p.discount) AS avg_discount,
       COUNT(DISTINCT p.product_id) AS total_products
FROM vendor v
JOIN orders o ON v.vendor_id = o.created_by
JOIN product p ON o.product_id = p.product_id
GROUP BY v.vendor_id, v.name;
```

Note: Replace placeholder values (e.g., [customer_id], [order_id]) with actual values when executing queries.

## Installation

### Prerequisites
- Python 3.10 or higher
- MySQL Server
- Git (for cloning the repository)

### Setup Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a Python virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up the MySQL database:
- Ensure MySQL server is running
- Create a database named 'EcommerceDB'
- Run the schema.sql script to create the necessary tables

5. Configure database connection:
- Open `db_connection.py`
- Update the database connection parameters if needed:
  - host (default: "localhost")
  - user (default: "root")
  - password (update as per your MySQL setup)
  - database (default: "EcommerceDB")

## Running the Application

1. Ensure your MySQL server is running

2. Start the Streamlit application:
```bash
streamlit run app.py
```

3. Access the application in your web browser (typically at http://localhost:8501)

## Usage

1. Select a query from the sidebar menu
2. Enter required parameters (e.g., customer ID, order ID)
3. View results in a formatted table
4. Use the interface to navigate between different functionalities

## Database Schema

The application uses a relational database with the following main tables:
- customer: Stores customer information
- product: Contains product details
- vendor: Manages vendor information
- orders: Tracks order details
- category: Manages product categories
- profile: Links customers to their addresses and payment methods
- payment: Stores payment information
- address: Contains address details

## Technologies Used

- Python 3.10
- Streamlit 1.28.2
- Pandas 2.1.3
- MySQL Connector Python 8.2.0
- MySQL Database

## Contributing

Feel free to submit issues and enhancement requests! 


