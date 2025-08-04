import sqlite3

DB_NAME = "cms.db"

class SaleDAO:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    # Create a sale and its items in a transaction
    def create(self, sale: dict, items: list[dict]) -> bool:
        """
        sale: {
            'sale_id': str,
            'customer_id': str,
            'date': str,
            'mode': 'Online' or 'Offline',
            'total_amount': float,
            'total_volume_points': int,
        }
        items: list of {
            'stock_no': str,
            'quantity': int,
            'price_per_unit': float,
            'total_amount': float,
            'volume_points': int,
            'pro_earned': float,
        }
        """
        try:
            conn = self._connect()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO Sale (
                    sale_id, customer_id, date, mode, total_amount, total_volume_points
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                sale['sale_id'], sale['customer_id'], sale['date'], sale['mode'],
                sale['total_amount'], sale['total_volume_points']
            ))

            for item in items:
                cursor.execute('''
                    INSERT INTO SaleItem (
                        sale_id, stock_no, quantity, price_per_unit, total_amount,
                        volume_points, pro_earned
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sale['sale_id'], item['stock_no'], item['quantity'], item['price_per_unit'],
                    item['total_amount'], item.get('volume_points', 0), item.get('pro_earned', 0.0)
                ))

            conn.commit()
            return True
        except Exception as e:
            print("Error creating sale:", e)
            return False
        finally:
            conn.close()

    def get(self, sale_id: str):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Sale WHERE sale_id = ?", (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            conn.close()
            return None

        cursor.execute("SELECT * FROM SaleItem WHERE sale_id = ?", (sale_id,))
        items = cursor.fetchall()
        conn.close()

        return {
            "sale": dict(sale),
            "items": [dict(item) for item in items]
        }

    def delete(self, sale_id: str) -> bool:
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Sale WHERE sale_id = ?", (sale_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    # Add update methods as needed...

    def list_all(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sale")
        sales = cursor.fetchall()
        conn.close()
        return [dict(s) for s in sales]
