import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import re
import sqlite3

PRODUCTS_DB_PATH = 'db/products.db'

def remove_duplicates():
    conn = sqlite3.connect(PRODUCTS_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    if cursor.fetchone() is None:
        print("Error: products.db")
        conn.close()
        return

    cursor.execute('''
    CREATE TABLE temp_products AS
    SELECT *
    FROM products
    WHERE rowid IN (
        SELECT MIN(rowid)
        FROM products
        GROUP BY product_id
    )
    ''')

    cursor.execute('DROP TABLE products')
    cursor.execute('''
    CREATE TABLE products (
        product_id TEXT PRIMARY KEY,
        url TEXT,
        sku TEXT,
        title TEXT
    )
    ''')

    cursor.execute('''
    INSERT INTO products (product_id, url, sku, title)
    SELECT product_id, url, sku, title
    FROM temp_products
    ''')

    cursor.execute('DROP TABLE temp_products')
    conn.commit()
    conn.close()

def web_dr_wu():
    base_url = "https://www.drwu.com/categories/category?page="
    page = 1

    conn = sqlite3.connect(PRODUCTS_DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        url TEXT,
        sku TEXT,
        title TEXT
    )
    ''')

    while True:
        url = base_url + str(page)
        response = requests.get(url, headers={"User-Agent": UserAgent().random})
        
        if response.status_code != 200:
            print(f"Finished scraping. Total pages: {page - 1}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('a', class_='quick-cart-item')

        if not products:
            print(f"No more products found. Finished at page {page - 1}")
            break

        for product in products:
            product_url = product.get('href')
            ng_click = product.get('ng-click')
            ga_product = product.get('ga-product')

            product_id = product_sku = product_title = None

            if ga_product:
                ga_product_dict = json.loads(ga_product.replace("'", '"'))
                product_id = ga_product_dict.get('id')
                product_sku = ga_product_dict.get('sku')
                product_title = ga_product_dict.get('title')

            if ng_click and (not product_id or not product_sku or not product_title):
                ng_click_parts = re.findall(r'"([^"]*)"', ng_click)
                if len(ng_click_parts) >= 3:
                    product_id = ng_click_parts[0]
                    product_sku = ng_click_parts[1]
                    product_title = ng_click_parts[2]

            if product_id:
                try:
                    cursor.execute('''
                    INSERT INTO products (product_id, url, sku, title) VALUES (?, ?, ?, ?)
                    ''', (product_id, product_url, product_sku, product_title))
                except sqlite3.IntegrityError:
                    # 如果 product_id 已存在，则跳过插入
                    print(f"Product {product_id} already exists. Skipping insertion.")
                    continue

        print(f"Scraped page {page}")
        page += 1

    conn.commit()
    conn.close()

