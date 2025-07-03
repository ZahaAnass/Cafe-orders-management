from database.database import connect_db, init_db

def connection():
    conn = connect_db()
    init_db()
    cursor = conn.cursor()
    return conn, cursor

def createCustomer(customer):
    conn, cursor = connection()
    query = """INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)"""
    cursor.execute(query, (customer["name"], customer["email"], customer["phone"]))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def updateCustomer(id, customer):
    conn, cursor = connection()
    query = """UPDATE customers SET name = %s, email = %s, phone = %s WHERE id = %s"""
    cursor.execute(query, (customer["name"], customer["email"], customer["phone"], id))
    conn.commit()
    conn.close()
    return cursor.rowcount

def deleteCustomer(id):
    conn, cursor = connection()
    query = """DELETE FROM customers WHERE id = %s"""
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
    return cursor.rowcount

def createProduct(product):
    conn, cursor = connection()
    query = """INSERT INTO products (name, price) VALUES (%s, %s)"""
    cursor.execute(query, (product["name"], product["price"]))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def updateProduct(id, product):
    conn, cursor = connection()
    query = """UPDATE products SET name = %s, price = %s WHERE id = %s"""
    cursor.execute(query, (product["name"], product["price"], id))
    conn.commit()
    conn.close()
    return cursor.rowcount

def deleteProduct(id):
    conn, cursor = connection()
    query = """DELETE FROM products WHERE id = %s"""
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
    return cursor.rowcount

def getTable():
    conn, cursor = connection()
    query = """
        SELECT 
            o.id as order_id,
            o.created_at as date,
            c.name as client, 
            c.phone as phone,
            GROUP_CONCAT(CONCAT(p.name, ' (', oi.quantity, 'x)') SEPARATOR ', ') as articles,
            SUM(p.price * oi.quantity) as total,
            o.status 
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        GROUP BY o.id, c.name, c.phone, o.created_at, o.status
        ORDER BY o.created_at DESC
    """
    cursor.execute(query)
    orders = cursor.fetchall()
    conn.close()
    return orders

def createOrder(order):
    conn, cursor = connection()
    query = """INSERT INTO orders (customer_id) VALUES (%s)"""
    cursor.execute(query, (order["customer_id"],))
    order_id = cursor.lastrowid
    for item in order["items"]:
        query = """INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"""
        cursor.execute(query, (order_id, item["product_id"], item["quantity"]))
    conn.commit()
    conn.close()
    return order_id

def updateOrder(id, order):
    conn, cursor = connection()
    query = """UPDATE orders SET customer_id = %s WHERE id = %s"""
    cursor.execute(query, (order["customer_id"], id))
    query = """DELETE FROM order_items WHERE order_id = %s"""
    cursor.execute(query, (id,))
    for item in order["items"]:
        query = """INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"""
        cursor.execute(query, (id, item["product_id"], item["quantity"]))
    conn.commit()
    conn.close()
    return cursor.rowcount

def deleteOrder(id):
    conn, cursor = connection()
    query = """DELETE FROM orders WHERE id = %s"""
    cursor.execute(query, (id,))
    query = """DELETE FROM order_items WHERE order_id = %s"""
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
    return cursor.rowcount

def createOrderItem(order_item):
    conn, cursor = connection()
    query = """INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"""
    cursor.execute(query, (order_item["order_id"], order_item["product_id"], order_item["quantity"]))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def updateOrderItem(id, order_item):
    conn, cursor = connection()
    query = """UPDATE order_items SET order_id = %s, product_id = %s, quantity = %s WHERE id = %s"""
    cursor.execute(query, (order_item["order_id"], order_item["product_id"], order_item["quantity"], id))
    conn.commit()
    conn.close()
    return cursor.rowcount

def deleteOrderItem(id):
    conn, cursor = connection()
    query = """DELETE FROM order_items WHERE id = %s"""
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
    return cursor.rowcount

def get_all_products():
    conn, cursor = connection()
    query = """SELECT * FROM products"""
    cursor.execute(query)
    products = cursor.fetchall()
    conn.close()
    return products

def get_orders_stats():
    conn, cursor = connection()
    # Total orders
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]
    # Total revenue: sum of all order_items price * quantity
    cursor.execute("""
        SELECT COALESCE(SUM(p.price * oi.quantity), 0)
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
    """)
    total_revenue = cursor.fetchone()[0] or 0
    conn.close()
    return {'total_orders': total_orders, 'total_revenue': total_revenue}