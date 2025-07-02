from database.database import connect_db

class Report:
    def __init__(self):
        self.db = connect_db()

    def get_data(self, start_date, product_category):
        cursor = self.db.cursor()
        query = """SELECT o.id, o.created_at, o.customer_id, o.status, SUM(oi.quantity * p.price) as total
                    FROM orders o
                    JOIN order_items oi ON o.id = oi.order_id
                    JOIN products p ON oi.product_id = p.id
                    WHERE o.created_at >= %s
                    AND p.category = %s
                    GROUP BY o.id"""
        cursor.execute(query, (start_date, product_category))
        return cursor.fetchall()

    def sales_by_day(self):
        cursor = self.db.cursor()
        query = """SELECT DATE(created_at) as date, SUM(price * quantity) as total
                    FROM orders o
                    JOIN order_items oi ON o.id = oi.order_id
                    JOIN products p ON p.id = oi.product_id
                    GROUP BY date"""
        cursor.execute(query)
        return cursor.fetchall()

    def sales_by_week(self):
        cursor = self.db.cursor()
        query = """SELECT WEEK(created_at) as week, SUM(price * quantity) as total
                    FROM orders o
                    JOIN order_items oi ON o.id = oi.order_id
                    JOIN products p ON p.id = oi.product_id
                    GROUP BY week"""
        cursor.execute(query)
        return cursor.fetchall()

    def sales_by_month(self):
        cursor = self.db.cursor()
        query = """SELECT MONTH(created_at) as month, SUM(price * quantity) as total
                    FROM orders o
                    JOIN order_items oi ON o.id = oi.order_id
                    JOIN products p ON p.id = oi.product_id
                    GROUP BY month"""
        cursor.execute(query)
        return cursor.fetchall()

    def most_popular_products(self, limit=10):
        cursor = self.db.cursor()
        query = """SELECT p.name, SUM(oi.quantity) as quantity
                    FROM orders o
                    JOIN order_items oi ON o.id = oi.order_id
                    JOIN products p ON p.id = oi.product_id
                    GROUP BY p.name
                    ORDER BY quantity DESC
                    LIMIT %s"""
        cursor.execute(query, (limit,))
        return cursor.fetchall()
