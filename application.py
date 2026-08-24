from flask import Flask, request, jsonify
import psycopg2
from scraper import get_product_info
from scheduler import schedule
from apscheduler.schedulers.background import BackgroundScheduler
import os

app=Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=5432, dbname="pricetracker",
        user="postgres", password="yourpassword"
    )

@app.route("/products", methods=["POST"])
def add_product():
    url = request.json["url"]
    info = get_product_info(url)
    price = info["price"]
    name = info["name"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (url, name) VALUES (%s, %s) RETURNING product_id",
        (url, name)
    )
    product_id = cursor.fetchone()[0]
    cursor.execute(
        "INSERT INTO product_history (product_id, price) VALUES (%s, %s)",
        (product_id, price)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"product_id": product_id, "name": name, "price": price})

@app.route("/products", methods=["GET"])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    rowList = []
    for row in rows:
        rowList.append({"product_id": row[0], "url": row[1], "name": row[2]})

    return jsonify (rowList)

@app.route("/products/<int:product_id>/history", methods=["GET"])
def get_history(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM product_history WHERE product_id = %s", (product_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    rowList = []
    for row in rows:
        rowList.append({"id": row[0], "product_id": row[1], "price": row[2], "timestamp": row[3]})

    return jsonify (rowList)

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM product_history WHERE product_id = %s", (product_id,))
    cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    conn.commit()
    cur.close()    
    conn.close()

    return jsonify({"message": f"Product {product_id} deleted"})


    
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule, "interval", minutes=60)
    scheduler.start()
    print("Scheduler started successfully")
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
