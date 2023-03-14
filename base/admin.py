from django.contrib import admin
from .models import Customer, Address, Category, Food, Item, Order

# Register your models here.
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Item)
admin.site.register(Order)
