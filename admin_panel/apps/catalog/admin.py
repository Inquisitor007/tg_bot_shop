from django.contrib import admin

from apps.catalog.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'created', 'update', 'subcategory']
    search_fields = ['name', 'description']
    list_filter = ['available', 'created', 'update','subcategory']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']
