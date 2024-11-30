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


