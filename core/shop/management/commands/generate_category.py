from faker import Faker
from shop.models import ProductCategoryModel
from django.core.management.base import BaseCommand
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Generate Fake Data For ProductCategory"

    def handle(self, *args, **kwargs):
        faker= Faker()

        for _ in range(10):
            title= faker.word()
            slug= slugify(title, allow_unicode=True)
            ProductCategoryModel.objects.get_or_create(title=title, slug=slug)

        self.stdout.write(self.style.SUCCESS(
            "Successfully generated 10 fake categories."
        ))