from django.contrib import admin
from .models import ProductModel, ProductImageModel, ProductCategoryModel, FavoritesProductModel
# Register your models here.

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=("id", "title", "stock", "status", "created_date")

@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display=("id", "title", "created_date")

@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display=("id", "file", "product","created_date")

@admin.register(FavoritesProductModel)
class FavoritesProductModelAdmin(admin.ModelAdmin):
    list_display=("id", "user", "product")
