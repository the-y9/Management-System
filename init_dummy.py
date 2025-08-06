import sqlite3
import csv
import os
import random
from datetime import datetime, timedelta

DB_NAME = "dummy.db"
PRODUCT_CSV = "products1.csv"
DUMMY_PRODUCTS_COUNT = 50
DUMMY_CUSTOMERS_COUNT = 100
DUMMY_SALES_COUNT = 300

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # --- TABLE CREATION ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            sno INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT,
            qty_per_unit TEXT,
            volume_points REAL,
            mrp REAL,
            retail_price REAL,
            earn_base REAL,
            per_25 REAL,
            per_35 REAL,
            per_42 REAL,
            per_50 REAL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            join_date DATE,
            notes TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sale (
            sale_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            date DATE NOT NULL,
            mode TEXT CHECK (mode IN ('Online', 'Offline')),
            total_amount REAL NOT NULL,
            total_volume_points INTEGER,
            FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SaleItem (
            sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id TEXT NOT NULL,
            stock_no TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            total_amount REAL NOT NULL,
            volume_points INTEGER,
            pro_earned REAL,
            FOREIGN KEY(sale_id) REFERENCES Sale(sale_id) ON DELETE CASCADE,
            FOREIGN KEY(stock_no) REFERENCES Product(stock_no)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LevelSlab (
            month TEXT PRIMARY KEY,
            total_sales REAL,
            total_volume_points INTEGER,
            slab_reached TEXT CHECK (slab_reached IN ('25%', '35%', '42%', '50%'))
        );
    ''')

    conn.commit()
    print("Tables created successfully.")

    # --- PRODUCT IMPORT OR DUMMY CREATION ---
    if os.path.exists(PRODUCT_CSV):
        with open(PRODUCT_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = [
                (
                    row['Stock No.'],
                    row['Product Name'],
                    row.get('Category', ''),
                    row['Qty.'],
                    safe_float(row['Volume Points']),
                    safe_float(row['MRP']),
                    safe_float(row['Retail Price']),
                    safe_float(row['*Earn Base']),
                    safe_float(row['Associates - 25%']),
                    safe_float(row['Senior Consultant - 35%']),
                    safe_float(row['Qualified Producer/ Success Builder - 42%']),
                    safe_float(row['Supervisor - 50%'])
                )
                for row in reader
            ]
            cursor.executemany('''
                INSERT OR REPLACE INTO Product (
                    stock_no, name, category, qty_per_unit,
                    volume_points, mrp, retail_price, earn_base,
                    per_25, per_35, per_42, per_50
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', rows)
            conn.commit()
            print(f"{len(rows)} products loaded from CSV.")
    else:
        print(f"No CSV found at {PRODUCT_CSV}. Creating dummy products...")
        dummy_products = []
        for i in range(1, DUMMY_PRODUCTS_COUNT + 1):
            stock_no = f"P{i:04d}"
            name = f"Product {i}"
            category = random.choice(["Health", "Beauty", "Fitness"])
            qty = f"{random.randint(100, 500)}g"
            vp = round(random.uniform(10, 50), 2)
            mrp = round(random.uniform(100, 500), 2)
            retail_price = round(mrp * 0.9, 2)
            earn_base = round(vp * 2, 2)
            per_25 = round(earn_base * 0.25, 2)
            per_35 = round(earn_base * 0.35, 2)
            per_42 = round(earn_base * 0.42, 2)
            per_50 = round(earn_base * 0.50, 2)
            dummy_products.append((stock_no, name, category, qty, vp, mrp, retail_price, earn_base, per_25, per_35, per_42, per_50))

        cursor.executemany('''
            INSERT INTO Product (
                stock_no, name, category, qty_per_unit,
                volume_points, mrp, retail_price, earn_base,
                per_25, per_35, per_42, per_50
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', dummy_products)
        conn.commit()
        print(f"{DUMMY_PRODUCTS_COUNT} dummy products created.")

    # --- CREATE DUMMY CUSTOMERS ---
    print("Creating dummy customers...")
    dummy_customers = []
    for i in range(1, DUMMY_CUSTOMERS_COUNT + 1):
        customer_id = f"CUST{i:03d}"
        name = f"Customer {i}"
        phone = f"98765432{i:02d}"
        email = f"customer{i}@test.com"
        address = f"{i} Demo Street, Test City"
        join_date = datetime.now() - timedelta(days=random.randint(30, 365))
        notes = "Test data"
        dummy_customers.append((customer_id, name, phone, email, address, join_date.strftime("%Y-%m-%d"), notes))

    cursor.executemany('''
        INSERT INTO Customer (customer_id, name, phone, email, address, join_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', dummy_customers)
    conn.commit()
    print(f"{DUMMY_CUSTOMERS_COUNT} dummy customers created.")

    # --- FETCH DATA FOR RELATIONSHIPS ---
    cursor.execute("SELECT customer_id FROM Customer")
    customer_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT stock_no, volume_points, retail_price FROM Product")
    product_rows = cursor.fetchall()

    # --- CREATE DUMMY SALES ---
    print("Creating dummy sales and sale items...")

    for i in range(1, DUMMY_SALES_COUNT + 1):
        sale_id = f"SAL{i:04d}"
        customer_id = random.choice(customer_ids)
        sale_date = datetime.now() - timedelta(days=random.randint(1, 90))
        mode = random.choice(['Online', 'Offline'])

        items_count = random.randint(1, 5)
        selected_products = random.sample(product_rows, min(items_count, len(product_rows)))

        total_amount = 0.0
        total_volume_points = 0
        sale_items_data = []

        for product in selected_products:
            stock_no, vp_per_unit, price = product
            quantity = random.randint(1, 3)
            total_price = round(quantity * price, 2)
            total_amount += total_price
            total_vp = int(vp_per_unit * quantity)
            total_volume_points += total_vp
            pro_earned = round(total_price * 0.25, 2)

            sale_items_data.append((
                sale_id, stock_no, quantity, price, total_price, total_vp, pro_earned
            ))

        # Insert sale
        cursor.execute('''
            INSERT INTO Sale (sale_id, customer_id, date, mode, total_amount, total_volume_points)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sale_id, customer_id, sale_date.strftime("%Y-%m-%d"), mode, total_amount, total_volume_points))

        # Insert sale items
        cursor.executemany('''
            INSERT INTO SaleItem (sale_id, stock_no, quantity, price_per_unit, total_amount, volume_points, pro_earned)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sale_items_data)


    conn.commit()
    print(f"{DUMMY_SALES_COUNT} dummy sales with items created.")

    conn.close()

if __name__ == "__main__":
    create_database()
