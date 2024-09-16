from django.contrib import admin

from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')

@admin.register(ClothingProduct)
class ClothingProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')
    filter_horizontal = ('sizes',)  
    
    
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','image',)
    
    
    

admin.register(Customer)
admin.register(Order)
admin.register(OrderItem)
