from django.utils.text import slugify
from faker import Faker
from django.core.management.base import BaseCommand
from shop.models import ProductModel, ProductCategoryModel, ProductStatusType
from accounts.models import User, UserType
from decimal import Decimal
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import requests
import random



class Command(BaseCommand):
    help = 'Generate fake products for the ProductModel'

    def handle(self, *args, **kwargs):
        # Creating fake categories first, if they don't already exist
        faker = Faker()

        for _ in range(10):  # Creating 10 fake products, change this number as needed
            title = faker.bs().title()
            description = faker.text()
            slug = slugify(title)
            users= User.objects.create_user(email=faker.email(),password=faker.password())

            image_url = f"https://picsum.photos/200/200?random={random.randint(1, 1000)}"
            response = requests.get(image_url)

            image = Image.open(BytesIO(response.content))

            image_size = len(response.content)

            if image_size > 1048576:  # 1MB
                image = self.resize_image(image)

            image_file = self.save_image(image)

            product = ProductModel(
                user=users,  # Example User IDs (adjust accordingly)
                title=title,
                slug=slug,
                image=image_file,
                description=description,
                stock=random.randint(1, 100),
                status=random.choice(ProductStatusType.choices)[0],  # Example status values (0: draft, 1: published, 2: archived)
                price=faker.random_int(min=10000, max=100000),
                discount_percent= faker.random_int(min=0,max=50),  # Discount percentage between 0 and 50
            )

            # Randomly assign categories to products

            product.save()

            self.stdout.write(self.style.SUCCESS(f"Created Product: {product.title}"))



    def resize_image(self, image):
        image = image.resize((800, 800), Image.ANTIALIAS)
        return image

    def save_image(self, image):
        img_io = BytesIO()
        image.save(img_io, format="JPEG", quality=85)
        img_io.seek(0)
        return ContentFile(img_io.read(), name="image.jpg")
