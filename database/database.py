import sqlite3

def create_database():
    conn = sqlite3.connect('cafe.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        table_number INTEGER,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total REAL DEFAULT 0
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price_per_unit REAL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )''')
    
    # Insert sample products if none exist
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ('Coffee', 3.5),
            ('Tea', 2.5),
            ('Sandwich', 5.0),
            ('Cake', 3.0)
        ]
        cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", sample_products)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database created successfully!")