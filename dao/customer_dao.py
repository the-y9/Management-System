# dao/customer_dao.py

import sqlite3
from typing import List, Dict, Optional
from config_db import DB_NAME

# DB_NAME = "cms.db"

class CustomerDAO:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, customer: Dict) -> bool:
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Customer (
                    customer_id, name, phone, email, address, join_date, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer['customer_id'], customer['name'],
                customer.get('phone'), customer.get('email'),
                customer.get('address'), customer.get('join_date'),
                customer.get('notes')
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print("Insert error:", e)
            return False
        finally:
            conn.close()

    def get(self, customer_id: str) -> Optional[Dict]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customer WHERE customer_id = ?", (customer_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def update(self, customer_id: str, updates: Dict) -> bool:
        if not updates:
            return False
        try:
            conn = self._connect()
            cursor = conn.cursor()
            fields = ', '.join(f"{k} = ?" for k in updates)
            values = list(updates.values()) + [customer_id]
            cursor.execute(f"UPDATE Customer SET {fields} WHERE customer_id = ?", values)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete(self, customer_id: str) -> bool:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customer WHERE customer_id = ?", (customer_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    def list_all(self) -> List[Dict]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customer")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
