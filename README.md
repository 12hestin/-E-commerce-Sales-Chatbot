# E-commerce Chatbot Platform

A modern e-commerce platform with an integrated AI chatbot to assist customers with their shopping experience. Built with React, Flask, and SQLite.

## 🌟 Features

- **User Authentication**
  - Secure registration and login
  - JWT-based session management
  - Password hashing for security

- **Product Management**
  - Browse product catalog
  - View detailed product information
  - Product image gallery
  - Price filtering

- **Shopping Cart**
  - Add/remove products
  - Update quantities
  - Real-time total calculation

- **AI Chatbot Assistant**
  - Natural language product search
  - Price inquiries
  - Product recommendations
  - Category-based filtering
  - Context-aware responses

## 🛠️ Technology Stack

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- Lucide Icons
- Vite

### Backend
- Python 3.8+
- Flask
- SQLite3
- JWT Authentication
- CORS support

## 📋 Prerequisites

- Node.js 16+
- Python 3.8+
- pip

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-chatbot
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## 🔧 Configuration

### Backend Configuration
- JWT secret key (in `app.py`)
- Database settings
- CORS settings

### Frontend Configuration
- API endpoint configuration
- Authentication settings
- Vite configuration

## 📁 Project Structure

```
ecommerce-chatbot/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── utils/
│       └── chat_handler.py # Chatbot logic
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.tsx       # Main application component
│   │   └── main.tsx      # Application entry point
│   ├── package.json
│   └── index.html
└── README.md
```

## 🔒 Security Features

- Password hashing using Werkzeug
- JWT token-based authentication
- Protected API endpoints
- CORS protection
- SQL injection prevention

## 🤖 Chatbot Features

The integrated chatbot can:
- Search products by name or category
- Provide price information
- Offer product recommendations
- Answer general inquiries
- Maintain context during conversations

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Products
- `GET /api/products` - Get all products
- `GET /api/cart` - Get user's cart
- `POST /api/cart/add` - Add item to cart

### Chat
- `POST /api/chat` - Send message to chatbot

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- [Your Name] - Initial work

## 🙏 Acknowledgments

- React team for the amazing framework
- Flask team for the robust backend framework
- Tailwind CSS for the utility-first CSS framework"# -E-commerce-Sales-Chatbot" 
