import sqlite3
import csv
import os

DB_NAME = "cms.db"
PRODUCT_CSV = "products.csv"

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0  # or None if you prefer


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create Product table with sno as PRIMARY KEY and stock_no as TEXT
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

    # Customer table remains unchanged
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

    # Sale table with foreign key to Customer
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sale (
        sale_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        date DATE NOT NULL,
        mode TEXT CHECK (mode IN ('Online', 'Offline')),
        total_amount REAL NOT NULL,
        total_volume_points INTEGER,

        FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
    );''')

    # SaleItem table with sale_id as foreign key
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

    # Level Slab table remains unchanged
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

    # Load product data from CSV
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
        print(f"No CSV found at {PRODUCT_CSV} — skipping product import.")

    conn.close()

if __name__ == "__main__":
    create_database()
