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
    cursor = conn.cursor(dictionary=True)
except Error as e:
    st.error(f"Failed to connect to the database: {str(e)}")
    st.stop()

# Sidebar with main navigation
st.sidebar.title("Navigation")
main_options = st.sidebar.radio(
    "Select Operation Type:",
    ["Basic Queries", "Advanced Analytics", "Data Management"]
)

if main_options == "Basic Queries":
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

elif main_options == "Advanced Analytics":
    advanced_option = st.sidebar.selectbox(
        "Choose Analysis:",
        [
            "Vendor Performance Dashboard",
            "Product Analytics",
            "Customer Insights",
            "Payment Analytics"
        ]
    )

    if advanced_option == "Vendor Performance Dashboard":
        st.header("Vendor Performance Analytics")
        
        # Vendor selection
        cursor.execute("SELECT vendor_id, name FROM vendor")
        vendors = cursor.fetchall()
        vendor_options = {v['name']: v['vendor_id'] for v in vendors}
        selected_vendor = st.selectbox("Select Vendor", options=list(vendor_options.keys()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Order Statistics")
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT o.order_id) as total_orders,
                    COUNT(DISTINCT o.customer_id) as unique_customers,
                    COALESCE(SUM(o.quantity), 0) as total_items_sold
                FROM vendor v
                LEFT JOIN orders o ON v.vendor_id = o.created_by
                WHERE v.vendor_id = %s
            """, (vendor_options[selected_vendor],))
            stats = cursor.fetchone()
            if stats:
                st.metric("Total Orders", int(stats['total_orders'] or 0))
                st.metric("Unique Customers", int(stats['unique_customers'] or 0))
                st.metric("Total Items Sold", int(stats['total_items_sold'] or 0))
        
        with col2:
            st.subheader("Product Performance")
            cursor.execute("""
                SELECT p.name as product_name,
                       COUNT(o.order_id) as order_count,
                       SUM(o.quantity) as total_quantity
                FROM vendor v
                JOIN orders o ON v.vendor_id = o.created_by
                JOIN product p ON o.product_id = p.product_id
                WHERE v.vendor_id = %s
                GROUP BY p.name
                ORDER BY order_count DESC
                LIMIT 5
            """, (vendor_options[selected_vendor],))
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.bar_chart(df.set_index('product_name')['order_count'])

    elif advanced_option == "Product Analytics":
        st.header("Product Performance Analytics")
        
        # Category filter
        cursor.execute("SELECT category_id, name FROM category")
        categories = cursor.fetchall()
        category_options = {cat['name']: cat['category_id'] for cat in categories}
        selected_category = st.selectbox("Filter by Category", options=['All'] + list(category_options.keys()))
        
        # Time range filter
        col1, col2 = st.columns(2)
        with col1:
            min_discount = st.slider("Minimum Discount", 0.0, 1.0, 0.0)
        
        # Query construction
        query = """
            SELECT p.name, p.description,
                   COUNT(o.order_id) as times_ordered,
                   SUM(o.quantity) as total_quantity,
                   p.discount,
                   c.name as category_name
            FROM product p
            LEFT JOIN orders o ON p.product_id = o.product_id
            LEFT JOIN category c ON p.category_id = c.category_id
            WHERE p.discount >= %s
        """
        params = [min_discount]
        
        if selected_category != 'All':
            query += " AND c.category_id = %s"
            params.append(category_options[selected_category])
        
        query += " GROUP BY p.product_id, p.name, p.description, p.discount, c.name ORDER BY times_ordered DESC"
        
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
            
            # Visualization
            st.subheader("Top Products by Orders")
            chart_data = df.nlargest(10, 'times_ordered')
            st.bar_chart(chart_data.set_index('name')['times_ordered'])

    elif advanced_option == "Customer Insights":
        st.header("Customer Behavior Analysis")
        
        # Customer search
        search_term = st.text_input("Search Customer by Name or Email")
        if search_term:
            cursor.execute("""
                SELECT c.customer_id, c.name, c.email,
                       COUNT(DISTINCT o.order_id) as total_orders,
                       COUNT(DISTINCT v.vendor_id) as vendors_used
                FROM customer c
                LEFT JOIN orders o ON c.customer_id = o.customer_id
                LEFT JOIN vendor v ON o.created_by = v.vendor_id
                WHERE c.name LIKE %s OR c.email LIKE %s
                GROUP BY c.customer_id, c.name, c.email
            """, (f"%{search_term}%", f"%{search_term}%"))
            results = cursor.fetchall()
            if results:
                st.dataframe(pd.DataFrame(results))
        
        # Overall customer statistics
        st.subheader("Customer Statistics")
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT c.customer_id) as total_customers,
                AVG(order_counts.order_count) as avg_orders_per_customer
            FROM customer c
            LEFT JOIN (
                SELECT customer_id, COUNT(*) as order_count
                FROM orders
                GROUP BY customer_id
            ) order_counts ON c.customer_id = order_counts.customer_id
        """)
        stats = cursor.fetchone()
        if stats:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Customers", int(stats['total_customers']))
            with col2:
                st.metric("Average Orders per Customer", round(float(stats['avg_orders_per_customer'] or 0), 2))

    elif advanced_option == "Payment Analytics":
        st.header("Payment Method Analysis")
        
        # Payment method statistics
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT p.payment_id) as total_payment_methods,
                COUNT(DISTINCT pr.customer_id) as customers_with_payment
            FROM payment p
            LEFT JOIN profile pr ON p.payment_id = pr.primary_payment_id
        """)
        stats = cursor.fetchone()
        if stats:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Payment Methods", stats['total_payment_methods'])
            with col2:
                st.metric("Customers with Payment", stats['customers_with_payment'])
        
        # Payment methods per customer
        st.subheader("Customer Payment Details")
        cursor.execute("""
            SELECT c.name as customer_name,
                   p.card_number,
                   p.expiration_date,
                   CASE WHEN pr.primary_payment_id = p.payment_id 
                        THEN 'Primary' ELSE 'Secondary' END as status
            FROM customer c
            JOIN profile pr ON c.customer_id = pr.customer_id
            JOIN payment p ON pr.primary_payment_id = p.payment_id
            ORDER BY c.name
        """)
        results = cursor.fetchall()
        if results:
            st.dataframe(pd.DataFrame(results))

elif main_options == "Data Management":
    management_option = st.sidebar.selectbox(
        "Choose Operation:",
        [
            "Manage Products",
            "Manage Categories",
            "Manage Vendors"
        ]
    )

    if management_option == "Manage Products":
        st.header("Product Management")
        
        # Add new product form
        with st.expander("Add New Product"):
            with st.form("new_product_form"):
                name = st.text_input("Product Name")
                description = st.text_area("Description")
                quantity = st.number_input("Quantity", min_value=1, value=1)
                discount = st.number_input("Discount (0-1)", min_value=0.0, max_value=1.0, value=0.0)
                
                # Get categories for dropdown
                cursor.execute("SELECT category_id, name FROM category")
                categories = cursor.fetchall()
                category_options = {cat['name']: cat['category_id'] for cat in categories}
                selected_category = st.selectbox("Category", options=list(category_options.keys()))
                
                if st.form_submit_button("Add Product"):
                    try:
                        cursor.execute("""
                            INSERT INTO product (name, description, quantity, discount, category_id)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (name, description, quantity, discount, category_options[selected_category]))
                        conn.commit()
                        st.success("Product added successfully!")
                    except Error as e:
                        st.error(f"Error adding product: {str(e)}")
        
        # View/Edit existing products
        st.subheader("Existing Products")
        cursor.execute("""
            SELECT p.product_id, p.name, p.description, p.quantity, p.discount,
                   c.name as category
            FROM product p
            LEFT JOIN category c ON p.category_id = c.category_id
        """)
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)

    elif management_option == "Manage Categories":
        st.header("Category Management")
        
        # Add new category
        with st.form("new_category_form"):
            category_name = st.text_input("Category Name")
            if st.form_submit_button("Add Category"):
                try:
                    cursor.execute("INSERT INTO category (name) VALUES (%s)", (category_name,))
                    conn.commit()
                    st.success("Category added successfully!")
                except Error as e:
                    st.error(f"Error adding category: {str(e)}")
        
        # View existing categories
        st.subheader("Existing Categories")
        cursor.execute("""
            SELECT c.name, COUNT(p.product_id) as product_count
            FROM category c
            LEFT JOIN product p ON c.category_id = p.category_id
            GROUP BY c.category_id, c.name
        """)
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)

    elif management_option == "Manage Vendors":
        st.header("Vendor Management")
        
        # Add new vendor
        with st.form("new_vendor_form"):
            vendor_name = st.text_input("Vendor Name")
            hotline = st.text_input("Hotline")
            description = st.text_area("Description")
            if st.form_submit_button("Add Vendor"):
                try:
                    cursor.execute("""
                        INSERT INTO vendor (name, hotline, description)
                        VALUES (%s, %s, %s)
                    """, (vendor_name, hotline, description))
                    conn.commit()
                    st.success("Vendor added successfully!")
                except Error as e:
                    st.error(f"Error adding vendor: {str(e)}")
        
        # View existing vendors
        st.subheader("Existing Vendors")
        cursor.execute("""
            SELECT v.name, v.hotline, v.description,
                   COUNT(DISTINCT o.order_id) as total_orders
            FROM vendor v
            LEFT JOIN orders o ON v.vendor_id = o.created_by
            GROUP BY v.vendor_id, v.name, v.hotline, v.description
        """)
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)

# Cleanup
try:
    cursor.close()
    conn.close()
except:
    pass 