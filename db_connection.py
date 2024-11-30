import mysql.connector
from mysql.connector import Error

def get_connection():
    """Get a connection to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="lusining123",
            database="EcommerceDB"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        raise e

class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="lusining123", database="EcommerceDB"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish connection to the MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                self.cursor = self.connection.cursor()
                return True
                
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("MySQL connection closed")

    def test_connection(self):
        """Test the database connection by executing a simple query"""
        try:
            if self.connect():
                # Test query to get table names
                self.cursor.execute("SHOW TABLES")
                tables = self.cursor.fetchall()
                
                print("\nAvailable tables in the database:")
                for table in tables:
                    print(f"- {table[0]}")
                
                return True
        except Error as e:
            print(f"Error testing connection: {e}")
            return False
        finally:
            self.disconnect()

def main():
    # Create database connection instance
    db = DatabaseConnection()
    
    # Test the connection
    print("Testing database connection...")
    success = db.test_connection()
    
    if success:
        print("\nDatabase connection test completed successfully")
    else:
        print("\nDatabase connection test failed")

if __name__ == "__main__":
    main() 