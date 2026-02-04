from django.core.management.base import BaseCommand
from faker import Faker
import random

from apps.products.models import Category, Product
from apps.stores.models import Store, Inventory

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with dummy data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Create Categories
        categories = []
        category_names = [
            "Electronics", "Clothing", "Home & Garden", "Sports", 
            "Books", "Food & Beverages", "Toys", "Beauty", "Furniture", "Automotive"
        ]
        
        for name in category_names:
            category, _ = Category.objects.get_or_create(name=name)
            categories.append(category)
        
        self.stdout.write(f"Created {len(categories)} categories")

        # Create Products
        products = []
        product_adjectives = [
            "Premium", "Professional", "Compact", "Deluxe", "Standard",
            "Advanced", "Basic", "Ultra", "Super", "Mega"
        ]
        product_nouns = [
            "Laptop", "Phone", "Tablet", "Camera", "Monitor",
            "Keyboard", "Mouse", "Headphones", "Speaker", "Router",
            "Printer", "Scanner", "Charger", "Cable", "Adapter"
        ]
        
        for i in range(1000):
            adjective = random.choice(product_adjectives)
            noun = random.choice(product_nouns)
            title = f"{adjective} {noun} {i}"
            
            product = Product.objects.create(
                title=title,
                description=fake.sentence(nb_words=10),
                price=round(random.uniform(10, 1000), 2),
                category=random.choice(categories),
            )
            products.append(product)
        
        self.stdout.write(f"Created {len(products)} products")

        # Create Stores
        stores = []
        for i in range(20):
            store = Store.objects.create(
                name=f"{fake.company()} Store {i}",
                location=fake.city(),
            )
            stores.append(store)
        
        self.stdout.write(f"✓ Created {len(stores)} stores")

        # Create Inventory
        inventory_count = 0
        for store in stores:
            store_products = random.sample(products, 300)
            for product in store_products:
                Inventory.objects.create(
                    store=store,
                    product=product,
                    quantity=random.randint(1, 100),
                )
                inventory_count += 1
        
        self.stdout.write(f"✓ Created {inventory_count} inventory items")
        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))