# dao/product_dao.py

import sqlite3
from typing import List, Dict, Optional

DB_NAME = "cms.db"

class ProductDAO:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # return dict-like rows
        return conn

    def create(self, product: Dict) -> bool:
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Product (
                    stock_no, name, category, qty_per_unit,
                    volume_points, mrp, retail_price, earn_base,
                    per_25, per_35, per_42, per_50
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product['stock_no'], product['name'], product.get('category', ''),
                product.get('qty_per_unit', ''), product.get('volume_points', 0.0),
                product.get('mrp', 0.0), product.get('retail_price', 0.0),
                product.get('earn_base', 0.0), product.get('per_25', 0.0),
                product.get('per_35', 0.0), product.get('per_42', 0.0),
                product.get('per_50', 0.0)
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print("Insert error:", e)
            return False
        finally:
            conn.close()

    def get(self, stock_no: str) -> Optional[Dict]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product WHERE stock_no = ?", (stock_no,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def update(self, stock_no: str, updates: Dict) -> bool:
        if not updates:
            return False
        try:
            conn = self._connect()
            cursor = conn.cursor()
            fields = ', '.join(f"{k} = ?" for k in updates)
            values = list(updates.values()) + [stock_no]
            cursor.execute(f"UPDATE Product SET {fields} WHERE stock_no = ?", values)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete(self, stock_no: str) -> bool:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Product WHERE stock_no = ?", (stock_no,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    def list_all(self) -> List[Dict]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
