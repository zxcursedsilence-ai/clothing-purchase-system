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


# ============================================================================
# ЗАДАЧА 3: АДМИНИСТРАТИВНЫЕ КЛАССЫ ДЛЯ POSTGRESQL МОДЕЛЕЙ
# ============================================================================

@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'delivery_time_days', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['icon_preview']
    
    def icon_preview(self, obj):
        if obj.icon:
            return f'<img src="{obj.icon.url}" style="max-height: 100px;" />'
        return 'Нет изображения'
    icon_preview.allow_tags = True
    icon_preview.short_description = 'Предпросмотр иконки'


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'address', 'birth_date', 'created_at']
    search_fields = ['buyer__first_name', 'buyer__last_name', 'address']
    list_filter = ['created_at']
    readonly_fields = ['photo_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('buyer', 'photo', 'photo_preview', 'passport_scan')
        }),
        ('Дополнительная информация', {
            'fields': ('address', 'birth_date', 'preferred_delivery_time', 'notes')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" style="max-height: 200px;" />'
        return 'Нет фото'
    photo_preview.allow_tags = True
    photo_preview.short_description = 'Предпросмотр фото'


class OrderItemInline(admin.TabularInline):
    """Inline для позиций заказа"""
    model = OrderItem
    extra = 1
    fields = ['assortment', 'quantity', 'unit_price', 'discount_percent', 'size', 'notes']
    readonly_fields = []


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'buyer', 'seller', 'delivery_method', 'status', 
                    'order_date', 'total_amount', 'delivery_cost']
    list_filter = ['status', 'order_date', 'delivery_method']
    search_fields = ['order_number', 'buyer__first_name', 'buyer__last_name', 
                     'delivery_address', 'contact_phone']
    readonly_fields = ['order_date', 'order_time', 'created_at', 'updated_at', 
                       'invoice_preview', 'delivery_photo_preview']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('order_number', 'buyer', 'seller', 'delivery_method', 'status')
        }),
        ('Даты и время', {
            'fields': ('order_date', 'order_time', 'delivery_date', 'delivery_time')
        }),
        ('Финансовые данные', {
            'fields': ('total_amount', 'delivery_cost', 'discount_percent')
        }),
        ('Доставка', {
            'fields': ('delivery_address', 'contact_phone')
        }),
        ('Файлы', {
            'fields': ('invoice_file', 'invoice_preview', 'delivery_confirmation_photo', 
                      'delivery_photo_preview')
        }),
        ('Дополнительно', {
            'fields': ('notes',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def invoice_preview(self, obj):
        if obj.invoice_file:
            return f'<a href="{obj.invoice_file.url}" target="_blank">Открыть файл</a>'
        return 'Нет файла'
    invoice_preview.allow_tags = True
    invoice_preview.short_description = 'Счет'
    
    def delivery_photo_preview(self, obj):
        if obj.delivery_confirmation_photo:
            return f'<img src="{obj.delivery_confirmation_photo.url}" style="max-height: 200px;" />'
        return 'Нет фото'
    delivery_photo_preview.allow_tags = True
    delivery_photo_preview.short_description = 'Фото подтверждения доставки'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'assortment', 'quantity', 'unit_price', 'size', 'get_subtotal']
    list_filter = ['order__status', 'size']
    search_fields = ['order__order_number', 'assortment__name']
    
    def get_subtotal(self, obj):
        return obj.get_subtotal()
    get_subtotal.short_description = 'Подытог'