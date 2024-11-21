import random
from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = "Seed the database with initial categories and products"

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write("Deleting old data...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Seed categories
        self.stdout.write("Seeding categories...")
        categories = [
            {"name": "Electronics", "description": "Devices and gadgets."},
            {"name": "Books", "description": "Fiction and non-fiction books."},
            {"name": "Toys", "description": "Kids' toys and games."},
            {"name": "Furniture", "description": "Home and office furniture."},
        ]

        category_objects = []
        for category in categories:
            category_objects.append(Category(**category))
        Category.objects.bulk_create(category_objects)

        # Seed products
        self.stdout.write("Seeding products...")
        products = [
            {"name": "Smartphone", "description": "Latest smartphone model.", "price": 699.99},
            {"name": "Laptop", "description": "High-performance laptop.", "price": 1299.99},
            {"name": "Tablet", "description": "Portable tablet device.", "price": 499.99},
            {"name": "Bookshelf", "description": "Wooden bookshelf.", "price": 89.99},
            {"name": "Board Game", "description": "Fun board game for kids.", "price": 29.99},
        ]

        category_ids = list(Category.objects.values_list("id", flat=True))
        product_objects = []
        for product in products:
            product["category_id"] = random.choice(category_ids)
            product_objects.append(Product(**product))
        Product.objects.bulk_create(product_objects)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))