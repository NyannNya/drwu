import sqlite3

# 資料庫路徑
DB_PATH = 'db/product_vertex.db'

def create_table():
    """Creates the image_descriptions table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS image_descriptions (
            url TEXT PRIMARY KEY,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_description(url):
    """
    Retrieves the description for a given URL from the database.
    Returns the description if found, else None.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT description FROM image_descriptions WHERE url = ?', (url,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_description(url, description):
    """Saves the URL and its description to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO image_descriptions (url, description)
        VALUES (?, ?)
    ''', (url, description))
    conn.commit()
    conn.close()
