from django.contrib import admin

# Register your models here.
from .models import Category, SubCategory, Item, OrderItem, Order, Customer

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Customer)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin) :
    list_display =['id', 'created_at', 'get_items', 'get_total_price']

