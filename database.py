import sqlite3

def create_db():
    conn = sqlite3.connect('shopping_list.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            purchased BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(email, username, password):
    conn = sqlite3.connect('shopping_list.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, password))
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = sqlite3.connect('shopping_list.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def username_exists(username):
    conn = sqlite3.connect('shopping_list.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def add_item(user_id, item_name, quantity, price):
    conn = sqlite3.connect('shopping_list.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shopping_list (user_id, item_name, quantity, price) VALUES (?, ?, ?, ?)", (user_id, item_name, quantity, price))
    conn.commit()
    conn.close()

def get_items(user_id):
    conn = sqlite3.connect('shopping_list.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shopping_list WHERE user_id=?", (user_id,))
    items = cursor.fetchall()
    conn.close()
    return items

def delete_item(item_id):
    conn = sqlite3.connect('shopping_list.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shopping_list WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

create_db()
