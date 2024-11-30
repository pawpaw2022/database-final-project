import streamlit as st
import pandas as pd
from db_connection import get_connection
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error

# Set page config
st.set_page_config(
    page_title="E-Commerce Database Interface",
    page_icon="🛍️",
    layout="wide"
)

# Title and welcome message
st.title("🛍️ E-Commerce Database Management System")
st.write("""
Welcome to our E-Commerce Database Management System! This application allows you to interact with our 
e-commerce database, view various analytics, and manage orders, products, and customer information.
""")

# Initialize database connection
try:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier DataFrame creation
except Error as e:
    st.error(f"Failed to connect to the database: {str(e)}")
    st.stop()

# Sidebar with query selection
st.sidebar.title("Available Queries")
query_option = st.sidebar.radio(
    "Select a query to execute:",
    [
        "1. Find Customer Orders",
        "2. List Products in Order",
        "3. Vendor Sales Report",
        "4. Customer Profile Info",
        "5. Product Categories",
        "6. Customer Payment Methods",
        "7. Product Search",
        "8. Vendor Information",
        "9. Popular Products",
        "10. Product Discounts",
        "11. Insert New Product"
    ]
)

try:
    # Main content area
    if "1. Find Customer Orders" in query_option:
        st.header("Find Orders by Customer")
        customer_id = st.text_input("Enter Customer ID")
        if st.button("Search Orders"):
            cursor.execute("""
                SELECT o.order_id, p.name as product_name, o.quantity, 
                       c.name as customer_name, v.name as vendor_name
                FROM orders o
                JOIN customer c ON o.customer_id = c.customer_id
                JOIN product p ON o.product_id = p.product_id
                JOIN vendor v ON o.created_by = v.vendor_id
                WHERE o.customer_id = %s
            """, (customer_id,))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.info("No orders found for this customer.")

    elif "2. List Products in Order" in query_option:
        st.header("List Products in Order")
        order_id = st.text_input("Enter Order ID")
        if st.button("Search Products"):
            cursor.execute("""
                SELECT p.product_id, p.name, p.description, o.quantity,
                       p.discount, cat.name as category
                FROM orders o
                JOIN product p ON o.product_id = p.product_id
                LEFT JOIN category cat ON p.category_id = cat.category_id
                WHERE o.order_id = %s
            """, (order_id,))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.info("No products found for this order.")

    elif "3. Vendor Sales Report" in query_option:
        st.header("Vendor Sales Report")
        vendor_id = st.text_input("Enter Vendor ID")
        if st.button("Generate Report"):
            cursor.execute("""
                SELECT v.name as vendor_name, p.name as product_name,
                       COUNT(o.order_id) as total_orders,
                       SUM(o.quantity) as total_quantity
                FROM vendor v
                JOIN orders o ON v.vendor_id = o.created_by
                JOIN product p ON o.product_id = p.product_id
                WHERE v.vendor_id = %s
                GROUP BY v.vendor_id, v.name, p.name
            """, (vendor_id,))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.info("No sales data found for this vendor.")

    elif "4. Customer Profile Info" in query_option:
        st.header("Customer Profile Information")
        customer_id = st.text_input("Enter Customer ID")
        if st.button("View Profile"):
            cursor.execute("""
                SELECT c.name, c.email, c.phone, c.bio,
                       a.street, a.city, a.zip_code,
                       p.card_number, p.expiration_date
                FROM customer c
                LEFT JOIN profile pr ON c.customer_id = pr.customer_id
                LEFT JOIN address a ON pr.primary_address_id = a.address_id
                LEFT JOIN payment p ON pr.primary_payment_id = p.payment_id
                WHERE c.customer_id = %s
            """, (customer_id,))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.info("No customer found with this ID.")

    elif "5. Product Categories" in query_option:
        st.header("Products by Category")
        cursor.execute("SELECT category_id, name FROM category")
        categories = cursor.fetchall()
        category_options = {cat['name']: cat['category_id'] for cat in categories}
        selected_category = st.selectbox("Select Category", options=list(category_options.keys()))
        
        if st.button("View Products"):
            cursor.execute("""
                SELECT p.name, p.description, p.quantity, p.discount,
                       c.name as category_name
                FROM product p
                JOIN category c ON p.category_id = c.category_id
                WHERE c.category_id = %s
            """, (category_options[selected_category],))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.info("No products found in this category.")

    elif "6. Customer Payment Methods" in query_option:
        st.header("Customer Payment Methods")
        customer_id = st.text_input("Enter Customer ID")
        if st.button("View Payment Methods"):
            cursor.execute("""
                SELECT c.name as customer_name,
                       pay.card_number, pay.expiration_date,
                       CASE WHEN pr.primary_payment_id = pay.payment_id 
                            THEN 'Primary' ELSE 'Secondary' END as payment_status
                FROM customer c
                JOIN profile pr ON c.customer_id = pr.customer_id
                JOIN payment pay ON pr.primary_payment_id = pay.payment_id
                WHERE c.customer_id = %s
            """, (customer_id,))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.info("No payment methods found for this customer.")

    elif "7. Product Search" in query_option:
        st.header("Product Search")
        search_term = st.text_input("Enter product name or description")
        if st.button("Search"):
            cursor.execute("""
                SELECT p.name, p.description, p.quantity, p.discount,
                       c.name as category_name
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                WHERE p.name LIKE %s OR p.description LIKE %s
            """, (f"%{search_term}%", f"%{search_term}%"))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.info("No products found matching your search.")

    elif "8. Vendor Information" in query_option:
        st.header("Vendor Information")
        vendor_id = st.text_input("Enter Vendor ID")
        if st.button("View Vendor Info"):
            cursor.execute("""
                SELECT v.name, v.hotline, v.description,
                       COUNT(DISTINCT o.order_id) as total_orders,
                       COUNT(DISTINCT o.customer_id) as unique_customers
                FROM vendor v
                LEFT JOIN orders o ON v.vendor_id = o.created_by
                WHERE v.vendor_id = %s
                GROUP BY v.vendor_id, v.name, v.hotline, v.description
            """, (vendor_id,))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.info("No vendor found with this ID.")

    elif "9. Popular Products" in query_option:
        st.header("Popular Products")
        st.write("Products ranked by number of orders")
        cursor.execute("""
            SELECT p.name, p.description,
                   COUNT(o.order_id) as times_ordered,
                   SUM(o.quantity) as total_quantity,
                   c.name as category_name
            FROM product p
            LEFT JOIN orders o ON p.product_id = o.product_id
            LEFT JOIN category c ON p.category_id = c.category_id
            GROUP BY p.product_id, p.name, p.description, c.name
            ORDER BY times_ordered DESC
            LIMIT 10
        """)
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.info("No order data available.")

    elif "10. Product Discounts" in query_option:
        st.header("Product Discounts")
        min_discount = st.slider("Minimum Discount", 0.0, 1.0, 0.1)
        if st.button("View Discounted Products"):
            cursor.execute("""
                SELECT p.name, p.description, p.quantity,
                       p.discount, c.name as category_name
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                WHERE p.discount <= %s
                ORDER BY p.discount ASC
            """, (min_discount,))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.info("No products found with the specified discount.")

    elif "11. Insert New Product" in query_option:
        st.header("Insert New Product")
        with st.form("new_product_form"):
            name = st.text_input("Product Name")
            description = st.text_area("Description")
            quantity = st.number_input("Quantity", min_value=1, value=1)
            discount = st.number_input("Discount (0-1)", min_value=0.0, max_value=1.0, value=1.0)
            
            # Get categories for dropdown
            cursor.execute("SELECT category_id, name FROM category")
            categories = cursor.fetchall()
            category_options = {cat['name']: cat['category_id'] for cat in categories}
            selected_category = st.selectbox("Category", options=list(category_options.keys()))
            
            if st.form_submit_button("Insert Product"):
                cursor.execute("""
                    INSERT INTO product (name, description, quantity, discount, category_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, description, quantity, discount, category_options[selected_category]))
                conn.commit()
                st.success("Product inserted successfully!")

except Error as e:
    st.error(f"Database error: {str(e)}")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

finally:
    # Footer
    st.markdown("---")
    st.markdown("© 2023 E-Commerce Database Management System")
    
    # Close database connection
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close() 