# Farm Fresh Website

A Django-based e-commerce website for fresh farm products with blog functionality and shopping cart features.

## Features

- Product catalog with categories
- Shopping cart functionality
- Blog section
- Contact form
- Responsive design

## Requirements

- Python 3.8+
- Django 4.2+
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/farming_website.git
cd farming_website
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit http://localhost:8000 in your browser.

## Usage

1. Admin Interface:
   - Access at `/admin`
   - Log in with superuser credentials
   - Manage products, categories, blog posts

2. Shopping:
   - Browse products
   - Add items to cart
   - Manage cart quantities

3. Blog:
   - Read blog posts
   - Filter by categories

## License

MIT License
