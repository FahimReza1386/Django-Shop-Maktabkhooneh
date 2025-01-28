from faker import Faker
from django.utils.text import slugify
from django.core.management.base import BaseCommand
from shop.models import ProductModel, ProductCategoryModel, ProductStatusType, ProductImageModel
from accounts.models import User
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import requests
import random

class Command(BaseCommand):
    help = 'Generate fake products'

    def handle(self, *args, **options):
        fake = Faker(locale="fa_IR")
        user= User.objects.create_user(email=fake.email(),password=fake.password())

        categories = ProductCategoryModel.objects.all()



        for _ in range(10):  # Generate 10 fake products
            user = user  
            num_categories = random.randint(1, 4)
            selected_categoreis = random.sample(list(categories), num_categories)
            title = ' '.join([fake.word() for _ in range(1,3)])
            slug = slugify(title,allow_unicode=True)
            description = fake.paragraph(nb_sentences=10)
            brief_description= fake.paragraph(nb_sentences=1)
            stock = fake.random_int(min=0, max=10)
            status = random.choice(ProductStatusType.choices)[0]  # Replace with your actual status choices
            price = fake.random_int(min=10000, max=100000)
            discount_percent = fake.random_int(min=0, max=50)


            image_url = f"https://picsum.photos/200/200?random={random.randint(1, 1000)}"
            response = requests.get(image_url)

            image = Image.open(BytesIO(response.content))

            image_size = len(response.content)

            if image_size > 1048576:  # 1MB
                image = self.resize_image(image)

            image_file = self.save_image(image)

            product = ProductModel.objects.create(
                user=user,
                title=title,
                slug=slug,
                image=image_file,
                description=description,
                brief_description=brief_description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent,
            )

            for _ in range(5):

                image_url = f"https://picsum.photos/200/200?random={random.randint(1, 1000)}"
                response = requests.get(image_url)

                image = Image.open(BytesIO(response.content))

                image_size = len(response.content)

                if image_size > 1048576:  # 1MB
                    image = self.resize_image(image)

                image_file = self.save_image(image)
                
                ProductImageModel.objects.create(product=product, file=image_file)


            product.category.set(selected_categoreis)
        
        
            

        self.stdout.write(self.style.SUCCESS('Successfully generated 10 fake products'))


    def resize_image(self, image):
        image = image.resize((800, 800), Image.ANTIALIAS)
        return image

    def save_image(self, image):
        img_io = BytesIO()
        image.save(img_io, format="JPEG", quality=85)
        img_io.seek(0)
        return ContentFile(img_io.read(), name="image.jpg")

