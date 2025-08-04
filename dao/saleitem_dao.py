import sqlite3

DB_NAME = "cms.db"

class SaleItemDAO:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, sale_id: str, item: dict) -> bool:
        """
        item keys: stock_no, quantity, price_per_unit, total_amount, volume_points, pro_earned
        """
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO SaleItem (
                    sale_id, stock_no, quantity, price_per_unit, total_amount, volume_points, pro_earned
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                sale_id,
                item['stock_no'],
                item['quantity'],
                item['price_per_unit'],
                item['total_amount'],
                item.get('volume_points', 0),
                item.get('pro_earned', 0.0)
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error creating SaleItem:", e)
            return False
        finally:
            conn.close()

    def get_by_id(self, sale_item_id: int) -> dict | None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SaleItem WHERE sale_item_id = ?", (sale_item_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_all_by_sale(self, sale_id: str) -> list[dict]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SaleItem WHERE sale_id = ?", (sale_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def update(self, sale_item_id: int, updated_fields: dict) -> bool:
        """
        updated_fields can include quantity, price_per_unit, total_amount, volume_points, pro_earned
        """
        try:
            conn = self._connect()
            cursor = conn.cursor()

            # Build SET clause dynamically
            set_clause = ", ".join([f"{k} = ?" for k in updated_fields.keys()])
            values = list(updated_fields.values())
            values.append(sale_item_id)

            sql = f"UPDATE SaleItem SET {set_clause} WHERE sale_item_id = ?"
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error updating SaleItem:", e)
            return False
        finally:
            conn.close()

    def delete(self, sale_item_id: int) -> bool:
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM SaleItem WHERE sale_item_id = ?", (sale_item_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error deleting SaleItem:", e)
            return False
        finally:
            conn.close()
