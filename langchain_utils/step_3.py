from langchain.schema import Document
import json
import sqlite3

def get_product_documents():
    conn1 = sqlite3.connect('db/products.db')
    cursor1 = conn1.cursor()
    query1 = '''
    SELECT url, title, product_id
    FROM products
    '''
    cursor1.execute(query1)
    product_rows = cursor1.fetchall()
    conn1.close()

    # product_details.db 查詢詳細資料
    conn2 = sqlite3.connect('db/product_details.db')
    cursor2 = conn2.cursor()
    query2 = '''
    SELECT url, description, image_urls 
    FROM product_details
    '''
    cursor2.execute(query2)
    detail_rows = cursor2.fetchall()
    conn2.close()

    # 將 products 和 product_details 資料合併
    detail_dict = {row[0]: row[1:] for row in detail_rows}
    documents = []

    for product in product_rows:
        url, title, product_id = product
        if url in detail_dict:
            description, image_urls = detail_dict[url]
            metadata = {'url': url, 'image_urls': image_urls}
            content = {'product_id' : product_id, 'title' : title, 'description': description}
            documents.append(Document(page_content=json.dumps(content), metadata=metadata))

    return documents