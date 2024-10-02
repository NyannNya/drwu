import sqlite3
from utils.scrape_details import web_dr_wu_details

# 資料庫路徑
PRODUCTS_DB_PATH = 'db/products.db'
DETAILS_DB_PATH = 'db/product_details.db'

def create_connection(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_details_table(conn):
    try:
        sql_create_details_table = """
        CREATE TABLE IF NOT EXISTS product_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            description TEXT,
            image_urls TEXT
        );
        """
        conn.execute(sql_create_details_table)
    except sqlite3.Error as e:
        print(e)

def insert_product_details(conn, product_details):
    try:
        sql_insert_details = """
        INSERT INTO product_details (url, description, image_urls)
        VALUES (?, ?, ?)
        """
        conn.execute(sql_insert_details, (product_details['url'], product_details['description'], ','.join(product_details['image_urls'])))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def fetch_all_urls(conn):
    try:
        cursor = conn.execute("SELECT url FROM products")
        rows = cursor.fetchall()
        return [row[0] for row in rows] 
    except sqlite3.Error as e:
        print(e)
        return []

# 主程式流程
def create():
    conn_products = create_connection(PRODUCTS_DB_PATH)

    if conn_products is not None:
        urls = fetch_all_urls(conn_products)
        conn_products.close()
    else:
        print("Error: products.db")
        return

    conn_details = create_connection(DETAILS_DB_PATH)

    if conn_details is not None:
        create_details_table(conn_details)
    else:
        print("Error: product_details.db")
        return

    for url in urls:
        result = web_dr_wu_details(url)
        
        if 'description' in result and 'image_urls' in result:
            product_details = {
                "url": url,
                "description": result["description"],
                "image_urls": result["image_urls"]
            }
            insert_product_details(conn_details, product_details)
        else:
            print(f"Error: URL: {url}, code: {result.get('status_code', 'Unknown')}")

    conn_details.close()

