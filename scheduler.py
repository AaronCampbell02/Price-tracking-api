from apscheduler.schedulers.background import BackgroundScheduler
import psycopg2
from scraper import get_product_info
import os


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=5432, dbname="pricetracker",
        user="postgres", password="yourpassword"
    )

def schedule():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    for row in rows:
        try:
            info = get_product_info(row[1])
            price = info["price"]
            product_id = row[0]
            cursor.execute("INSERT INTO product_history (product_id,price) VALUES (%s,%s)", (product_id, price))
        except Exception as e:
            print(f"Failed to scrape product {row[0]}: {e}")


    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    schedule()