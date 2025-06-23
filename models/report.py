class Report:
    def __init__(self, db):
        self.db = db

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
