from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import timedelta
from utils.chat_handler import ChatHandler

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)
chat_handler = ChatHandler()

# Database initialization
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create chat_history table
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create cart table
    c.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Mock data generation
def generate_mock_data():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    
    # Check if products already exist
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
        # Insert mock products
        products = [
            ('Laptop Pro', 'High-performance laptop for professionals', 1299.99, 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853'),
            ('Wireless Headphones', 'Premium noise-canceling headphones', 199.99, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e'),
            ('Smart Watch', 'Fitness and health tracking smartwatch', 299.99, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30'),
            ('Tablet Pro', 'Powerful tablet for creative professionals', 799.99, 'https://images.unsplash.com/photo-1585790050230-5dd28404ccb9'),
            ('Gaming Console', 'Next-gen gaming experience', 499.99, 'https://images.unsplash.com/photo-1486401899868-0e435ed85128'),
            ('Wireless Earbuds', 'True wireless earbuds with premium sound', 149.99, 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df'),
        ]
        c.executemany('INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)', products)
        conn.commit()
    
    conn.close()

# Generate mock data
generate_mock_data()

# Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        
        # Check if user exists
        c.execute('SELECT id FROM users WHERE email = ?', (data['email'],))
        if c.fetchone() is not None:
            return jsonify({'message': 'Email already registered'}), 400
        
        # Hash password and create user
        hashed_password = generate_password_hash(data['password'])
        c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                 (data['username'], data['email'], hashed_password))
        conn.commit()
        
        # Create access token
        access_token = create_access_token(identity=data['email'])
        
        return jsonify({
            'message': 'User registered successfully',
            'token': access_token
        }), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        
        # Get user
        c.execute('SELECT id, email, password FROM users WHERE email = ?', (data['email'],))
        user = c.fetchone()
        
        if user is None or not check_password_hash(user[2], data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Create access token
        access_token = create_access_token(identity=user[1])
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token
        })
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products', methods=['GET'])
@jwt_required()
def get_products():
    try:
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        
        c.execute('SELECT id, name, description, price, image FROM products')
        products = [{
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'price': row[3],
            'image': row[4]
        } for row in c.fetchall()]
        
        return jsonify(products)
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    user_email = get_jwt_identity()
    
    if 'message' not in data:
        return jsonify({'message': 'No message provided'}), 400
    
    try:
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        
        # Get user ID
        c.execute('SELECT id FROM users WHERE email = ?', (user_email,))
        user_id = c.fetchone()[0]
        
        # Generate response using ChatHandler
        user_message = data['message']
        response = chat_handler.generate_response(user_message)
        
        # Save chat history
        c.execute('INSERT INTO chat_history (user_id, message, response) VALUES (?, ?, ?)',
                 (user_id, user_message, response))
        conn.commit()
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    user_email = get_jwt_identity()
    
    if 'productId' not in data:
        return jsonify({'message': 'No product ID provided'}), 400
    
    try:
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        
        # Get user ID
        c.execute('SELECT id FROM users WHERE email = ?', (user_email,))
        user_id = c.fetchone()[0]
        
        # Add to cart
        c.execute('INSERT INTO cart (user_id, product_id) VALUES (?, ?)',
                 (user_id, data['productId']))
        conn.commit()
        
        return jsonify({'message': 'Product added to cart successfully'})
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_email = get_jwt_identity()
    
    try:
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        
        # Get user ID
        c.execute('SELECT id FROM users WHERE email = ?', (user_email,))
        user_id = c.fetchone()[0]
        
        # Get cart items with product details
        c.execute('''
            SELECT p.id, p.name, p.price, p.image, c.quantity
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
        ''', (user_id,))
        
        cart_items = [{
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'image': row[3],
            'quantity': row[4]
        } for row in c.fetchall()]
        
        return jsonify(cart_items)
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)