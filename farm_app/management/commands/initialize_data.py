from django.core.management.base import BaseCommand
from farm_app.models import Category, Product
from decimal import Decimal
from django.core.files import File
import os
import requests
from django.conf import settings

class Command(BaseCommand):
    help = 'Initialize categories and products for the farming website'

    def download_image(self, url, filename):
        media_path = os.path.join(settings.MEDIA_ROOT, 'products', filename)
        if not os.path.exists(media_path):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(media_path, 'wb') as f:
                        f.write(response.content)
                    return f'products/{filename}'
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Failed to download image: {e}'))
                return None
        return f'products/{filename}'

    def handle(self, *args, **kwargs):
        # Create Categories
        categories_data = [
            {
                'name': 'Vegetables',
                'description': 'Fresh, organic vegetables from local farms'
            },
            {
                'name': 'Fruits',
                'description': 'Sweet and fresh fruits from our orchards'
            },
            {
                'name': 'Dairy',
                'description': 'Fresh dairy products from local farms'
            },
            {
                'name': 'Grains',
                'description': 'Organic grains and cereals'
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category "{category.name}"'))

        # Create Products
        vegetables = Category.objects.get(name='Vegetables')
        fruits = Category.objects.get(name='Fruits')
        dairy = Category.objects.get(name='Dairy')
        grains = Category.objects.get(name='Grains')

        products_data = [
            {
                'name': 'Fresh Tomatoes',
                'description': 'Ripe, juicy tomatoes perfect for salads and cooking',
                'price': Decimal('2.99'),
                'category': vegetables,
                'stock': 100,
                'image_url': 'https://images.pexels.com/photos/533280/pexels-photo-533280.jpeg',
                'image_filename': 'tomatoes.jpg'
            },
            {
                'name': 'Organic Carrots',
                'description': 'Sweet and crunchy organic carrots',
                'price': Decimal('1.99'),
                'category': vegetables,
                'stock': 150,
                'image_url': 'https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg',
                'image_filename': 'carrots.jpg'
            },
            {
                'name': 'Fresh Spinach',
                'description': 'Nutrient-rich fresh spinach leaves',
                'price': Decimal('3.49'),
                'category': vegetables,
                'stock': 80,
                'image_url': 'https://images.pexels.com/photos/2325843/pexels-photo-2325843.jpeg',
                'image_filename': 'spinach.jpg'
            },
            {
                'name': 'Bell Peppers',
                'description': 'Colorful and crisp bell peppers',
                'price': Decimal('2.49'),
                'category': vegetables,
                'stock': 120,
                'image_url': 'https://images.pexels.com/photos/128536/pexels-photo-128536.jpeg',
                'image_filename': 'peppers.jpg'
            },
            {
                'name': 'Red Apples',
                'description': 'Sweet and crisp red apples from our orchards',
                'price': Decimal('3.99'),
                'category': fruits,
                'stock': 200,
                'image_url': 'https://images.pexels.com/photos/102104/pexels-photo-102104.jpeg',
                'image_filename': 'apples.jpg'
            },
            {
                'name': 'Fresh Strawberries',
                'description': 'Sweet and juicy strawberries',
                'price': Decimal('4.99'),
                'category': fruits,
                'stock': 75,
                'image_url': 'https://images.pexels.com/photos/46174/pexels-photo-46174.jpeg',
                'image_filename': 'strawberries.jpg'
            },
            {
                'name': 'Ripe Bananas',
                'description': 'Fresh, perfectly ripe bananas',
                'price': Decimal('2.49'),
                'category': fruits,
                'stock': 150,
                'image_url': 'https://images.pexels.com/photos/1093038/pexels-photo-1093038.jpeg',
                'image_filename': 'bananas.jpg'
            },
            {
                'name': 'Sweet Oranges',
                'description': 'Juicy and sweet oranges',
                'price': Decimal('3.99'),
                'category': fruits,
                'stock': 100,
                'image_url': 'https://images.pexels.com/photos/327098/pexels-photo-327098.jpeg',
                'image_filename': 'oranges.jpg'
            },
            {
                'name': 'Organic Milk',
                'description': 'Fresh organic milk from grass-fed cows',
                'price': Decimal('3.49'),
                'category': dairy,
                'stock': 50,
                'image_url': 'https://images.pexels.com/photos/248412/pexels-photo-248412.jpeg',
                'image_filename': 'milk.jpg'
            },
            {
                'name': 'Farm Fresh Eggs',
                'description': 'Free-range eggs from happy chickens',
                'price': Decimal('4.49'),
                'category': dairy,
                'stock': 100,
                'image_url': 'https://images.pexels.com/photos/162712/egg-white-food-protein-162712.jpeg',
                'image_filename': 'eggs.jpg'
            },
            {
                'name': 'Artisan Cheese',
                'description': 'Handcrafted artisanal cheese',
                'price': Decimal('6.99'),
                'category': dairy,
                'stock': 40,
                'image_url': 'https://images.pexels.com/photos/821365/pexels-photo-821365.jpeg',
                'image_filename': 'cheese.jpg'
            },
            {
                'name': 'Greek Yogurt',
                'description': 'Creamy, protein-rich Greek yogurt',
                'price': Decimal('3.99'),
                'category': dairy,
                'stock': 60,
                'image_url': 'https://images.pexels.com/photos/1435735/pexels-photo-1435735.jpeg',
                'image_filename': 'yogurt.jpg'
            },
            {
                'name': 'Organic Quinoa',
                'description': 'Nutrient-rich organic quinoa',
                'price': Decimal('5.99'),
                'category': grains,
                'stock': 80,
                'image_url': 'https://images.pexels.com/photos/7421213/pexels-photo-7421213.jpeg',
                'image_filename': 'quinoa.jpg'
            },
            {
                'name': 'Brown Rice',
                'description': 'Wholesome organic brown rice',
                'price': Decimal('3.99'),
                'category': grains,
                'stock': 120,
                'image_url': 'https://images.pexels.com/photos/4110251/pexels-photo-4110251.jpeg',
                'image_filename': 'rice.jpg'
            },
            {
                'name': 'Steel Cut Oats',
                'description': 'Premium steel cut oats',
                'price': Decimal('4.49'),
                'category': grains,
                'stock': 90,
                'image_url': 'https://images.pexels.com/photos/216951/pexels-photo-216951.jpeg',
                'image_filename': 'oats.jpg'
            },
            {
                'name': 'Ancient Grains Mix',
                'description': 'Blend of ancient grains including amaranth and millet',
                'price': Decimal('6.99'),
                'category': grains,
                'stock': 70,
                'image_url': 'https://images.pexels.com/photos/1393382/pexels-photo-1393382.jpeg',
                'image_filename': 'ancient_grains.jpg'
            },
            {
                'name': 'Fresh Honey',
                'description': 'Pure, raw honey from local beekeepers',
                'price': Decimal('8.99'),
                'category': dairy,
                'stock': 45,
                'image_url': 'https://images.pexels.com/photos/1638280/pexels-photo-1638280.jpeg',
                'image_filename': 'honey.jpg'
            },
            {
                'name': 'Organic Avocados',
                'description': 'Creamy, ripe avocados perfect for any meal',
                'price': Decimal('5.99'),
                'category': vegetables,
                'stock': 60,
                'image_url': 'https://images.pexels.com/photos/557659/pexels-photo-557659.jpeg',
                'image_filename': 'avocados.jpg'
            }
        ]

        # Ensure media directory exists
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'products'), exist_ok=True)

        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'category': prod_data['category'],
                    'stock': prod_data['stock']
                }
            )
            
            # Download and set the image for both new and existing products
            image_path = self.download_image(prod_data['image_url'], prod_data['image_filename'])
            if image_path:
                product.image = image_path
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Updated product "{product.name}" with image'))
