import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

def connect_db():
    """Connect to MySQL database."""
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return mydb

def init_db():
    """Initialize tables in MySQL database."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            status VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)
    
    # Insert sample customers
    customers_data = [
        ('John Smith', 'john.smith@email.com', '+1-555-0101'),
        ('Sarah Johnson', 'sarah.johnson@email.com', '+1-555-0102'),
        ('Michael Brown', 'michael.brown@email.com', '+1-555-0103'),
        ('Emily Davis', 'emily.davis@email.com', '+1-555-0104'),
        ('David Wilson', 'david.wilson@email.com', '+1-555-0105'),
        ('Lisa Anderson', 'lisa.anderson@email.com', '+1-555-0106'),
        ('Robert Taylor', 'robert.taylor@email.com', '+1-555-0107'),
        ('Jennifer Martinez', 'jennifer.martinez@email.com', '+1-555-0108'),
        ('William Garcia', 'william.garcia@email.com', '+1-555-0109'),
        ('Amanda Rodriguez', 'amanda.rodriguez@email.com', '+1-555-0110'),
        ('James Thompson', 'james.thompson@email.com', '+1-555-0111'),
        ('Michelle White', 'michelle.white@email.com', '+1-555-0112'),
        ('Christopher Lee', 'christopher.lee@email.com', '+1-555-0113'),
        ('Ashley Clark', 'ashley.clark@email.com', '+1-555-0114'),
        ('Daniel Lewis', 'daniel.lewis@email.com', '+1-555-0115'),
        ('Jessica Walker', 'jessica.walker@email.com', '+1-555-0116'),
        ('Matthew Hall', 'matthew.hall@email.com', '+1-555-0117'),
        ('Nicole Allen', 'nicole.allen@email.com', '+1-555-0118'),
        ('Kevin Young', 'kevin.young@email.com', '+1-555-0119'),
        ('Stephanie King', 'stephanie.king@email.com', '+1-555-0120')
    ]
    
    cursor.executemany(
        "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
        customers_data
    )
    
    # Insert sample products
    products_data = [
        ('Wireless Headphones', 'Electronics', 89.99),
        ('Coffee Maker', 'Appliances', 129.99),
        ('Running Shoes', 'Sports', 79.99),
        ('Laptop Stand', 'Electronics', 45.99),
        ('Yoga Mat', 'Sports', 29.99),
        ('Bluetooth Speaker', 'Electronics', 59.99),
        ('Kitchen Knife Set', 'Kitchen', 99.99),
        ('Desk Lamp', 'Furniture', 39.99),
        ('Water Bottle', 'Sports', 19.99),
        ('Phone Case', 'Electronics', 24.99),
        ('Cookbook', 'Books', 34.99),
        ('Backpack', 'Accessories', 69.99),
        ('Wireless Mouse', 'Electronics', 29.99),
        ('Air Purifier', 'Appliances', 199.99),
        ('Tennis Racket', 'Sports', 149.99),
        ('Pillow', 'Home', 49.99),
        ('Tablet Stand', 'Electronics', 35.99),
        ('Protein Powder', 'Health', 54.99),
        ('Wall Clock', 'Home', 42.99),
        ('USB Cable', 'Electronics', 14.99)
    ]
    
    cursor.executemany(
        "INSERT INTO products (name, category, price) VALUES (%s, %s, %s)",
        products_data
    )
    
    # Insert sample orders
    orders_data = [
        (1, 'completed'),
        (2, 'pending'),
        (3, 'completed'),
        (4, 'shipped'),
        (5, 'completed'),
        (1, 'pending'),
        (6, 'completed'),
        (7, 'shipped'),
        (8, 'completed'),
        (9, 'pending'),
        (10, 'completed'),
        (2, 'shipped'),
        (11, 'completed'),
        (12, 'pending'),
        (13, 'completed'),
        (14, 'shipped'),
        (15, 'completed'),
        (3, 'pending'),
        (16, 'completed'),
        (17, 'shipped')
    ]
    
    cursor.executemany(
        "INSERT INTO orders (customer_id, status) VALUES (%s, %s)",
        orders_data
    )
    
    # Insert sample order items
    order_items_data = [
        (1, 1, 2),      # Order 1: 2x Wireless Headphones
        (1, 5, 1),      # Order 1: 1x Yoga Mat
        (2, 2, 1),      # Order 2: 1x Coffee Maker
        (3, 3, 1),      # Order 3: 1x Running Shoes
        (3, 9, 2),      # Order 3: 2x Water Bottle
        (4, 4, 1),      # Order 4: 1x Laptop Stand
        (5, 6, 1),      # Order 5: 1x Bluetooth Speaker
        (6, 1, 1),      # Order 6: 1x Wireless Headphones
        (7, 7, 1),      # Order 7: 1x Kitchen Knife Set
        (7, 8, 2),      # Order 7: 2x Desk Lamp
        (8, 10, 3),     # Order 8: 3x Phone Case
        (9, 11, 1),     # Order 9: 1x Cookbook
        (10, 12, 1),    # Order 10: 1x Backpack
        (11, 13, 2),    # Order 11: 2x Wireless Mouse
        (12, 14, 1),    # Order 12: 1x Air Purifier
        (13, 15, 1),    # Order 13: 1x Tennis Racket
        (14, 16, 4),    # Order 14: 4x Pillow
        (15, 17, 1),    # Order 15: 1x Tablet Stand
        (16, 18, 2),    # Order 16: 2x Protein Powder
        (17, 19, 1),    # Order 17: 1x Wall Clock
        (18, 20, 5),    # Order 18: 5x USB Cable
        (19, 2, 1),     # Order 19: 1x Coffee Maker
        (19, 8, 1),     # Order 19: 1x Desk Lamp
        (20, 3, 2)      # Order 20: 2x Running Shoes
    ]
    
    cursor.executemany(
        "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
        order_items_data
    )
    
    print("Database initialized with sample data!")
    print("- 20 customers added")
    print("- 20 products added") 
    print("- 20 orders added")
    print("- 24 order items added")

    conn.commit()
    conn.close()