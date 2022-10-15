from django.contrib import admin

from eshop.models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "description", "form")
    list_filter = ("category",)

class CategoryAdmin(admin.ModelAdmin):
   list_display = ("name", "id")
   list_filter = ("name",)



admin.site.register(Product, ProductAdmin)

admin.site.register(Category, CategoryAdmin)