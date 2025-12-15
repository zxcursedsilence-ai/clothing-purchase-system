"""
URL конфигурация для приложения firstapp_var_11.
Только CRUD операции для Задачи 2.
"""
from django.urls import path
from .views_crud import *
from django.views.generic import TemplateView
urlpatterns = [
    # ============================================================================
    # ЗАДАЧА 2.1: CRUD для одной таблицы (ClothesType)
    # ============================================================================
    path('clothestypes/', ClothesTypeListView.as_view(), name='clothestype_list'),
    path('clothestype/<int:pk>/', ClothesTypeDetailView.as_view(), name='clothestype_detail'),
    path('clothestype/create/', ClothesTypeCreateView.as_view(), name='clothestype_create'),
    path('clothestype/<int:pk>/update/', ClothesTypeUpdateView.as_view(), name='clothestype_update'),
    path('clothestype/<int:pk>/delete/', ClothesTypeDeleteView.as_view(), name='clothestype_delete'),

    # ============================================================================
    # ЗАДАЧА 2.2: CRUD для двух таблиц (1:M) - Buyer и Purchase
    # ============================================================================
    path('buyers-crud/', BuyerListView.as_view(), name='buyer_list'),
    path('buyer-crud/<int:pk>/', BuyerDetailView.as_view(), name='buyer_detail'),
    path('buyer-crud/create/', BuyerCreateView.as_view(), name='buyer_create'),
    path('buyer-crud/<int:pk>/update/', BuyerUpdateView.as_view(), name='buyer_update'),
    path('buyer-crud/<int:pk>/delete/', BuyerDeleteView.as_view(), name='buyer_delete'),

    # Покупки (CRUD)
    path('purchase-crud/create/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase-crud/<int:pk>/update/', PurchaseUpdateView.as_view(), name='purchase_update'),
    path('purchase-crud/<int:pk>/delete/', PurchaseDeleteView.as_view(), name='purchase_delete'),

    # ============================================================================
    # ЗАДАЧА 2.3: CRUD для трех таблиц (M:M) - Assortment
    # ============================================================================
    path('assortment-crud/', AssortmentListView.as_view(), name='assortment_list'),
    path('assortment-crud/<int:pk>/', AssortmentDetailView.as_view(), name='assortment_detail'),
    path('assortment-crud/create/', AssortmentCreateView.as_view(), name='assortment_create'),
    path('assortment-crud/<int:pk>/update/', AssortmentUpdateView.as_view(), name='assortment_update'),
    path('assortment-crud/<int:pk>/delete/', AssortmentDeleteView.as_view(), name='assortment_delete'),

    # ============================================================================
    # ЗАДАЧА 2.4: CRUD для двух таблиц (1:1) - Seller
    # ============================================================================
    path('sellers-crud/', SellerListView.as_view(), name='seller_list'),
    path('seller-crud/<int:pk>/', SellerDetailView.as_view(), name='seller_detail'),
    path('seller-crud/create/', SellerCreateView.as_view(), name='seller_create'),
    path('seller-crud/<int:pk>/update/', SellerUpdateView.as_view(), name='seller_update'),
    path('seller-crud/<int:pk>/delete/', SellerDeleteView.as_view(), name='seller_delete'),

    # ============================================================================
    # ДОПОЛНИТЕЛЬНЫЕ CRUD ОПЕРАЦИИ
    # ============================================================================

    # Размеры одежды (дополнительно)
    path('sizes-crud/',
         TemplateView.as_view(template_name='crud/size_list.html'),
         name='size_list'),

    # Управление наличием товаров по размерам
    path('assortment-size/create/',
         TemplateView.as_view(template_name='crud/assortmentsize_form.html'),
         name='assortmentsize_create'),
]