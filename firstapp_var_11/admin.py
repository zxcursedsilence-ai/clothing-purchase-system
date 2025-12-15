from django.contrib import admin
from .models import *

# Регистрация моделей для админ-панели

@admin.register(ClothesType)
class ClothesTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'phone', 'registration_date', 'is_vip']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['gender', 'is_vip']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'purchase_date', 'total_amount', 'payment_method']
    list_filter = ['payment_method', 'purchase_date']
    search_fields = ['buyer__first_name', 'buyer__last_name']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size_value', 'system', 'description']
    list_filter = ['system']
    search_fields = ['size_value']

@admin.register(Assortment)
class AssortmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'clothes_type', 'category', 'price', 'stock_quantity', 'created_at']
    list_filter = ['category', 'clothes_type']
    search_fields = ['name', 'description']

@admin.register(AssortmentSize)
class AssortmentSizeAdmin(admin.ModelAdmin):
    list_display = ['assortment', 'size', 'quantity']
    list_filter = ['size']

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'hire_date']
    search_fields = ['first_name', 'last_name', 'email']

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['seller', 'phone', 'department', 'experience_years']
    search_fields = ['seller__first_name', 'seller__last_name', 'phone']
