# Amigurumi Store 🧶

A beautiful e-commerce website for handcrafted amigurumi toys and accessories, built with Django REST Framework backend and React frontend.

## 🌟 Features

- **Modern Design**: Beautiful, responsive design inspired by contemporary e-commerce sites
- **Product Catalog**: Browse amigurumi products by categories (Animals, Dolls, Characters, Accessories, Seasonal)
- **Featured Products**: Showcase special and popular items
- **Product Details**: Detailed product pages with descriptions and features
- **Category Filtering**: Easy navigation through product categories
- **Mobile Responsive**: Optimized for all device sizes
- **RESTful API**: Clean API for product management and retrieval

## 🛠️ Tech Stack

### Backend
- **Django 4.2.7** - Python web framework
- **Django REST Framework** - API development
- **SQLite** - Database (easily changeable to PostgreSQL/MySQL)
- **Pillow** - Image processing
- **Django CORS Headers** - Cross-origin resource sharing

### Frontend
- **React 18** - JavaScript library for UI
- **React Router** - Navigation and routing
- **Axios** - HTTP client for API calls
- **CSS3** - Modern styling with gradients and animations
- **Google Fonts (Poppins)** - Typography

## 📁 Project Structure

```
amigurumi_store/
├── backend/
│   ├── amigurumi_store/        # Django project settings
│   ├── products/               # Products app
│   ├── media/amigurumi/       # Product images
│   ├── manage.py
│   ├── requirements.txt
│   └── populate_db.py         # Sample data script
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   └── ...
│   ├── package.json
│   └── yarn.lock
├── sample_*.jpg               # Sample product images
├── setup_backend.bat         # Windows backend setup
├── setup_frontend.bat        # Windows frontend setup
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Yarn package manager installed

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd amigurumi_store
```

### 2. Backend Setup (Windows)
```bash
# Run the setup script
setup_backend.bat

# Or manually:
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional
python populate_db.py
```

### 3. Frontend Setup (Windows)
```bash
# Run the setup script
setup_frontend.bat

# Or manually:
cd frontend
yarn install
```

### 4. Run the Applications

**Backend (Terminal 1):**
```bash
cd backend
venv\Scripts\activate  # If not already activated
python manage.py runserver
```
The API will be available at `http://localhost:8000`

**Frontend (Terminal 2):**
```bash
cd frontend
yarn start
```
The website will be available at `http://localhost:3000`

## 📊 API Endpoints

- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product by ID
- `GET /api/products/featured/` - Get featured products
- `GET /api/products/category/{category}/` - Get products by category
- `GET /admin/` - Django admin panel

## 🎨 Design Features

- **Modern Color Scheme**: Purple gradient theme with clean whites and grays
- **Card-based Layout**: Beautiful product cards with hover effects
- **Responsive Grid**: Automatic layout adjustment for different screen sizes
- **Smooth Animations**: CSS transitions and transforms for interactive elements
- **Typography**: Professional font hierarchy using Poppins font family
- **Category Icons**: Emoji-based category identification for visual appeal

## 🏷️ Product Categories

- 🐻 **Animals** - Cute animal amigurumi
- 👧 **Dolls** - Handmade character dolls
- 🦄 **Characters** - Fantasy and cartoon characters
- 🧶 **Accessories** - Useful and decorative items
- 🎄 **Seasonal** - Holiday and seasonal decorations

## 🖼️ Sample Data

The project includes 11 sample products with images showcasing:
- Orange fox amigurumi
- Green teddy bear
- Blue lace doilies
- Crocheted shawls
- Pink sheep
- Rainbow unicorns
- Character dolls
- Seasonal items

## 🔧 Customization

### Adding New Products
1. Use Django admin panel at `http://localhost:8000/admin/`
2. Upload product images and fill in details
3. Products automatically appear in the frontend

### Styling Changes
- Modify CSS files in `frontend/src/components/` and `frontend/src/pages/`
- Main color scheme can be changed in CSS custom properties
- Update `frontend/src/index.css` for global styles

### API Extensions
- Add new endpoints in `backend/products/views.py`
- Update URL patterns in `backend/products/urls.py`
- Extend the model in `backend/products/models.py`

## 🌐 Deployment

### Backend Deployment
1. Update `ALLOWED_HOSTS` in settings.py
2. Configure database settings for production
3. Set `DEBUG = False`
4. Configure static/media file serving
5. Use a proper WSGI server like Gunicorn

### Frontend Deployment
1. Update API base URL in `frontend/src/services/api.js`
2. Run `yarn build` to create production build
3. Serve the build folder with a web server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 💡 Future Enhancements

- Shopping cart functionality
- User authentication and profiles
- Payment integration
- Product reviews and ratings
- Search functionality
- Wishlist feature
- Email notifications
- Inventory management
- Multi-language support

## 📧 Contact

For questions or support, please contact:
- Email: hello@amigurumistore.com
- Phone: +1 (555) 123-4567

---

Made with ❤️ for craft lovers and amigurumi enthusiasts!
