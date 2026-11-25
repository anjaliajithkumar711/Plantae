
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'price',
        'is_featured'
    )

    list_filter = (
        'category',
        'is_featured'
    )

    search_fields = ('title', 'category')

    list_editable = ('price', 'is_featured')
