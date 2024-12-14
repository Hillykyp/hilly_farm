from django.core.management.base import BaseCommand
from farm_app.models import BlogPost
from django.utils.text import slugify
import requests
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Initialize blog posts'

    def handle(self, *args, **kwargs):
        blog_posts = [
            {
                'title': 'Sustainable Farming Practices for the Modern Era',
                'content': '''
                In today's rapidly changing world, sustainable farming practices are more important than ever. 
                This post explores various methods that modern farmers are using to ensure environmental sustainability 
                while maintaining productive yields.

                Key practices include:
                1. Crop Rotation
                2. Water Conservation
                3. Natural Pest Control
                4. Soil Management

                By implementing these practices, farmers can help preserve our environment for future generations while 
                producing high-quality, nutritious food for today's consumers.
                ''',
                'excerpt': 'Discover modern sustainable farming practices that are shaping the future of agriculture.',
                'image_url': 'https://images.pexels.com/photos/2132171/pexels-photo-2132171.jpeg',
                'is_featured': True
            },
            {
                'title': 'The Benefits of Organic Farming',
                'content': '''
                Organic farming has seen a surge in popularity over the past decade, and for good reason. 
                This article delves into the numerous benefits of organic farming practices.

                Benefits include:
                - Improved soil health
                - Better biodiversity
                - Reduced chemical exposure
                - Higher nutritional value

                Learn how organic farming practices can benefit both the environment and human health.
                ''',
                'excerpt': 'Explore the many advantages of organic farming for both consumers and the environment.',
                'image_url': 'https://images.pexels.com/photos/2286776/pexels-photo-2286776.jpeg',
                'is_featured': True
            },
            {
                'title': 'Farm to Table: Understanding the Journey',
                'content': '''
                The farm-to-table movement has revolutionized how we think about food. This post takes you through 
                the journey your food takes from our farm to your table.

                We'll explore:
                - Harvesting processes
                - Quality control measures
                - Transportation and storage
                - Local distribution networks

                Understanding this journey helps appreciate the value of local farming and fresh produce.
                ''',
                'excerpt': 'Follow the journey of fresh produce from our farm to your dinner table.',
                'image_url': 'https://images.pexels.com/photos/1268101/pexels-photo-1268101.jpeg',
                'is_featured': True
            },
            {
                'title': 'Seasonal Growing Guide: What to Plant When',
                'content': '''
                Success in farming and gardening largely depends on timing. This comprehensive guide helps you 
                understand what crops to plant during each season.

                Spring:
                - Leafy greens
                - Peas
                - Root vegetables

                Summer:
                - Tomatoes
                - Peppers
                - Cucumbers

                Fall:
                - Brassicas
                - Winter squash
                - Root crops

                Winter:
                - Indoor microgreens
                - Cold-hardy vegetables
                - Planning for spring
                ''',
                'excerpt': 'Learn the best times to plant different crops throughout the year.',
                'image_url': 'https://images.pexels.com/photos/2255801/pexels-photo-2255801.jpeg',
                'is_featured': False
            },
            {
                'title': 'The Rise of Urban Farming',
                'content': '''
                Urban farming is transforming cities and changing how we think about agriculture. This post 
                explores innovative urban farming techniques and their impact on food security.

                Topics covered:
                - Vertical farming
                - Rooftop gardens
                - Community gardens
                - Hydroponics and aquaponics

                Discover how urban farming is making fresh produce more accessible in cities while reducing 
                carbon footprints and building stronger communities.
                ''',
                'excerpt': 'Explore how urban farming is revolutionizing agriculture in cities.',
                'image_url': 'https://images.pexels.com/photos/2886937/pexels-photo-2886937.jpeg',
                'is_featured': False
            },
            {
                'title': 'Winter Gardening: Growing Food Year-Round',
                'content': '''
                Think the growing season ends with summer? Think again! Winter gardening opens up exciting 
                possibilities for year-round food production. This comprehensive guide explores techniques 
                and crops perfect for cold-weather cultivation.

                Essential Winter Gardening Tips:
                1. Choosing Cold-Hardy Varieties
                   - Kale
                   - Brussels Sprouts
                   - Winter Lettuce
                   - Root Vegetables

                2. Protection Methods
                   - Cold Frames
                   - Row Covers
                   - Greenhouse Options
                   - Mulching Techniques

                3. Timing Considerations
                   - When to Start Seeds
                   - Optimal Planting Windows
                   - Harvesting Schedules

                4. Soil Preparation
                   - Winter Soil Amendments
                   - Drainage Solutions
                   - Frost Protection

                By following these guidelines, you can enjoy fresh, homegrown produce even in the coldest months. 
                Winter gardening not only extends your growing season but also provides fresh, nutritious vegetables 
                when they're most expensive in stores.

                Remember: Success in winter gardening comes from proper planning and preparation. Start small, 
                learn from experience, and gradually expand your winter garden as you gain confidence.
                ''',
                'excerpt': 'Learn how to maintain a productive garden even during the winter months.',
                'image_url': 'https://images.pexels.com/photos/1408221/pexels-photo-1408221.jpeg',
                'is_featured': False
            }
        ]

        for post_data in blog_posts:
            # Create slug from title
            slug = slugify(post_data['title'])
            
            # Create or update blog post
            post, created = BlogPost.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': post_data['title'],
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'is_featured': post_data['is_featured']
                }
            )

            # Download and save image
            response = requests.get(post_data['image_url'])
            if response.status_code == 200:
                image_name = f"{slug}.jpg"
                post.image.save(image_name, ContentFile(response.content), save=True)
                self.stdout.write(self.style.SUCCESS(f'Updated blog post "{post.title}" with image'))
            else:
                self.stdout.write(self.style.WARNING(f'Failed to download image for "{post.title}"'))
