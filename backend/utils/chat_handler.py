from typing import List, Dict
import sqlite3

class ChatHandler:
    def __init__(self):
        self.db_path = 'ecommerce.db'

    def get_product_info(self, product_name: str) -> Dict:
        """Get detailed information about a specific product."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT id, name, description, price, image 
            FROM products 
            WHERE LOWER(name) LIKE ?
        ''', (f'%{product_name.lower()}%',))
        
        product = c.fetchone()
        conn.close()
        
        if product:
            return {
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'price': product[3],
                'image': product[4]
            }
        return None

    def get_products_by_category(self, category: str) -> List[Dict]:
        """Get products filtered by category."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT id, name, description, price, image 
            FROM products 
            WHERE LOWER(description) LIKE ?
        ''', (f'%{category.lower()}%',))
        
        products = [{
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'price': row[3],
            'image': row[4]
        } for row in c.fetchall()]
        
        conn.close()
        return products

    def generate_response(self, message: str) -> str:
        """Generate an appropriate response based on user input."""
        message = message.lower()
        
        # Check for product-specific queries
        product = self.get_product_info(message)
        if product:
            return f"📱 {product['name']}\n" \
                   f"💰 Price: ${product['price']}\n" \
                   f"📝 {product['description']}"

        # Check for category queries
        if any(category in message for category in ['electronics', 'tech', 'gadgets']):
            products = self.get_products_by_category('electronics')
            if products:
                response = "Here are our electronic products:\n\n"
                for product in products:
                    response += f"• {product['name']} - ${product['price']}\n"
                return response

        # Check for price queries
        if any(word in message for word in ['price', 'cost', 'how much']):
            return "Here are our current prices:\n" + \
                   "\n".join([f"• {p['name']}: ${p['price']}" 
                            for p in self.get_products_by_category('')])

        # Check for help or general queries
        if any(word in message for word in ['help', 'support', 'assist']):
            return ("I can help you with:\n"
                   "• Product information\n"
                   "• Prices\n"
                   "• Product recommendations\n"
                   "Just ask about any product or category!")

        # Default response with suggestion
        return ("I can provide information about our products. Try asking about:\n"
               "• Specific products (e.g., 'Tell me about the Smart Watch')\n"
               "• Prices (e.g., 'How much is the Laptop Pro?')\n"
               "• Categories (e.g., 'Show me electronics')")