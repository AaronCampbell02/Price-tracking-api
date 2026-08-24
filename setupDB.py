import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=5432, dbname="pricetracker",
        user="postgres", password="yourpassword"
    )
conn = get_db_connection()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        url TEXT NOT NULL,
        name TEXT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS product_history (
            id SERIAL PRIMARY KEY,
            product_id INTEGER REFERENCES products(product_id),
            price NUMERIC(10,2),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)



conn.commit()
cur.close()
conn.close()