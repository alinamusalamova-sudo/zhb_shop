from database import get_db

def create_user(username, email, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, email, password) 
        VALUES (%s, %s, %s) 
        RETURNING id
    ''', (username, email, password))
    user_id = cursor.fetchone()['id']
    conn.commit()
    cursor.close()
    conn.close()
    return user_id

def get_user(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def check_login(username, password):
    user = get_user(username)
    if user and user['password'] == password:
        return True
    return False

def get_all_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def add_product(name, description, price, user_id, image_url=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, description, price, user_id, image_url) 
        VALUES (%s, %s, %s, %s, %s) 
        RETURNING id
    ''', (name, description, price, user_id, image_url))
    product_id = cursor.fetchone()['id']
    conn.commit()
    cursor.close()
    conn.close()
    return product_id

def get_product_by_id(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return product

def update_product(product_id, name, description, price, image_url=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE products 
        SET name = %s, description = %s, price = %s, image_url = %s 
        WHERE id = %s
    ''', (name, description, price, image_url, product_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
    conn.commit()
    cursor.close()
    conn.close()

def create_order(product_id, user_id, quantity, contact_phone):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (product_id, user_id, quantity, contact_phone, status) 
        VALUES (%s, %s, %s, %s, 'new') 
        RETURNING id
    ''', (product_id, user_id, quantity, contact_phone))
    order_id = cursor.fetchone()['id']
    conn.commit()
    cursor.close()
    conn.close()
    return order_id

def get_orders_by_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.*, p.name as product_name, p.price 
        FROM orders o 
        JOIN products p ON o.product_id = p.id 
        WHERE o.user_id = %s 
        ORDER BY o.created_at DESC
    ''', (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders

def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_all_orders():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.*, p.name as product_name, u.username as customer_name 
        FROM orders o 
        JOIN products p ON o.product_id = p.id 
        JOIN users u ON o.user_id = u.id 
        ORDER BY o.created_at DESC
    ''')
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders

def get_all_categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories ORDER BY name')
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories

def get_product_categories(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.* FROM categories c 
        JOIN product_categories pc ON c.id = pc.category_id 
        WHERE pc.product_id = %s
    ''', (product_id,))
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories

def get_all_users_count():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()['count']
    cursor.close()
    conn.close()
    return count