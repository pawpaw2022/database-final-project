import pandas as pd
import mysql.connector
from datetime import datetime

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'lusining123',  # Replace with your MySQL password
    'database': 'EcommerceDB'
}

def connect_to_database():
    """Establish connection to the database"""
    try:
        connection = mysql.connector.connect(**db_config)
        print("Successfully connected to the database")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def insert_customers(connection):
    """Insert customer data from CSV"""
    try:
        # Read customer data with correct filename
        customers_df = pd.read_csv('data/customer.csv')
        cursor = connection.cursor()
        
        # Prepare insert statement
        insert_query = """
        INSERT INTO customer (customer_id, name, email, phone, bio)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        # Convert DataFrame to list of tuples
        customer_data = [tuple(row) for row in customers_df.values]
        
        # Execute batch insert
        cursor.executemany(insert_query, customer_data)
        connection.commit()
        
        print(f"Successfully inserted {len(customer_data)} customers")
        cursor.close()
        
    except Exception as e:
        print(f"Error inserting customer data: {e}")
        connection.rollback()

def insert_addresses(connection):
    """Insert address data from CSV"""
    try:
        # Read address data with correct filename
        addresses_df = pd.read_csv('data/address.csv')
        # Fill NaN values with None
        addresses_df = addresses_df.where(pd.notnull(addresses_df), None)
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO address (address_id, street, zip_code, city)
        VALUES (%s, %s, %s, %s)
        """
        
        address_data = [
            (row.address_id, row.street, row.zip_code, row.city)
            for _, row in addresses_df.iterrows()
            if None not in (row.address_id, row.street, row.zip_code, row.city)
        ]
        
        cursor.executemany(insert_query, address_data)
        connection.commit()
        
        print(f"Successfully inserted {len(address_data)} addresses")
        cursor.close()
        
    except Exception as e:
        print(f"Error inserting address data: {e}")
        connection.rollback()

def insert_payments(connection):
    """Insert payment data from CSV"""
    try:
        payments_df = pd.read_csv('data/payment.csv')
        # Ensure column names match exactly
        required_columns = ['payment_id', 'card_number', 'cvv', 'expiration_date']
        if not all(col in payments_df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")
            
        cursor = connection.cursor()
        
        # Convert expiration_date to proper format
        payments_df['expiration_date'] = pd.to_datetime(payments_df['expiration_date']).dt.strftime('%Y-%m-%d')
        
        # Prepare insert statement
        insert_query = """
        INSERT INTO payment (payment_id, card_number, cvv, expiration_date)
        VALUES (%s, %s, %s, %s)
        """
        
        # Convert DataFrame to list of tuples
        payment_data = [tuple(row) for row in payments_df.values]
        
        # Execute batch insert
        cursor.executemany(insert_query, payment_data)
        connection.commit()
        
        print(f"Successfully inserted {len(payment_data)} payments")
        cursor.close()
        
    except Exception as e:
        print(f"Error inserting payment data: {e}")
        connection.rollback()

def insert_categories(connection):
    """Insert category data from CSV"""
    try:
        categories_df = pd.read_csv('data/category.csv')
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO category (category_id, name)
        VALUES (%s, %s)
        """
        
        category_data = [tuple(row) for row in categories_df.values]
        cursor.executemany(insert_query, category_data)
        connection.commit()
        
        print(f"Successfully inserted {len(category_data)} categories")
        cursor.close()
        
    except Exception as e:
        print(f"Error inserting category data: {e}")
        connection.rollback()

def insert_profiles(connection):
    """Insert profile data from CSV"""
    try:
        profiles_df = pd.read_csv('data/profile.csv')
        # Convert numpy int64 to regular Python int
        profiles_df = profiles_df.astype(int)
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO profile (profile_id, customer_id, primary_address_id, primary_payment_id)
        VALUES (%s, %s, %s, %s)
        """
        
        profile_data = [tuple(map(int, row)) for row in profiles_df.values]
        cursor.executemany(insert_query, profile_data)
        connection.commit()
        
        print(f"Successfully inserted {len(profile_data)} profiles")
        cursor.close()
        
    except Exception as e:
        print(f"Error inserting profile data: {e}")
        connection.rollback()

def insert_products(connection):
    """Insert product data from CSV"""
    try:
        products_df = pd.read_csv('data/product.csv')
        # Convert category_id to int
        products_df['category_id'] = products_df['category_id'].astype(int)
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO product (product_id, name, description, quantity, discount, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        product_data = [(int(row[0]), str(row[1]), str(row[2]), int(row[3]), float(row[4]), int(row[5])) 
                        for row in products_df.values]
        cursor.executemany(insert_query, product_data)
        connection.commit()
        
        print(f"Successfully inserted {len(product_data)} products")
        cursor.close()
        
    except Exception as e:
        print(f"Error inserting product data: {e}")
        connection.rollback()

def insert_vendors(connection):
    """Insert vendor data from CSV"""
    try:
        vendors_df = pd.read_csv('data/vendor.csv')
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO vendor (vendor_id, name, hotline, description)
        VALUES (%s, %s, %s, %s)
        """
        
        vendor_data = [tuple(row) for row in vendors_df.values]
        cursor.executemany(insert_query, vendor_data)
        connection.commit()
        
        print(f"Successfully inserted {len(vendor_data)} vendors")
        cursor.close()
        
    except Exception as e:
        print(f"Error inserting vendor data: {e}")
        connection.rollback()

def insert_orders(connection):
    """Insert order data from CSV"""
    try:
        orders_df = pd.read_csv('data/order.csv')
        # Convert numeric columns to Python int
        orders_df = orders_df.astype({
            'order_id': int,
            'customer_id': int,
            'product_id': int,
            'created_by': int,
            'quantity': int
        })
        
        # Add current timestamp for each order
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO orders (order_id, customer_id, product_id, created_by, quantity, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Add timestamp to each order tuple
        order_data = [
            (*map(int, row), current_time) 
            for row in orders_df.values
        ]
        
        cursor.executemany(insert_query, order_data)
        connection.commit()
        
        print(f"Successfully inserted {len(order_data)} orders")
        cursor.close()
        
    except Exception as e:
        print(f"Error inserting order data: {e}")
        connection.rollback()

def clear_tables(connection):
    """Clear all tables in reverse order of dependencies"""
    try:
        cursor = connection.cursor()
        # Disable foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Clear tables in reverse order of dependencies
        tables = [
            'orders',
            'profile',
            'product',
            'vendor',
            'category',
            'payment',
            'address',
            'customer'
        ]
        
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table}")
            print(f"Cleared table: {table}")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        connection.commit()
        cursor.close()
        
    except Exception as e:
        print(f"Error clearing tables: {e}")
        connection.rollback()

def main():
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        # Clear all tables first
        # clear_tables(connection)
        
        # Then insert in correct order
        # insert_customers(connection)
        # insert_addresses(connection)
        # insert_payments(connection)
        # insert_categories(connection)
        # insert_products(connection)
        # insert_profiles(connection)
        # insert_vendors(connection)
        # insert_orders(connection)
        
        print("Data insertion completed successfully")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    main() 