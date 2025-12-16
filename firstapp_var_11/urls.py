from django.urls import path
from . import views, views_crud

# app_name убран, чтобы главная страница была доступна без префикса
# Если нужно использовать пространство имен, используйте 'clothing_app:' в шаблонах

urlpatterns = [
    # Главная страница определена в главном urls.py для доступности без префикса приложения

    # CRUD для покупателей (Buyer)
    path('customers/', views_crud.CustomerListView.as_view(), name='customer_list'),
    path('customers/new/', views_crud.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/', views_crud.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/edit/', views_crud.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', views_crud.CustomerDeleteView.as_view(), name='customer_delete'),
    
    # Альтернативные пути для Buyer
    path('buyers/', views_crud.BuyerListView.as_view(), name='buyer_list'),
    path('buyers/new/', views_crud.BuyerCreateView.as_view(), name='buyer_create'),
    path('buyers/<int:pk>/', views_crud.BuyerDetailView.as_view(), name='buyer_detail'),
    path('buyers/<int:pk>/edit/', views_crud.BuyerUpdateView.as_view(), name='buyer_update'),
    path('buyers/<int:pk>/delete/', views_crud.BuyerDeleteView.as_view(), name='buyer_delete'),

    # CRUD для продавцов
    path('sellers/', views_crud.SellerListView.as_view(), name='seller_list'),
    path('sellers/new/', views_crud.SellerCreateView.as_view(), name='seller_create'),
    path('sellers/<int:pk>/', views_crud.SellerDetailView.as_view(), name='seller_detail'),
    path('sellers/<int:pk>/edit/', views_crud.SellerUpdateView.as_view(), name='seller_update'),
    path('sellers/<int:pk>/delete/', views_crud.SellerDeleteView.as_view(), name='seller_delete'),

    # CRUD для типов одежды
    path('clothing-types/', views_crud.ClothingTypeListView.as_view(), name='clothing_type_list'),
    path('clothing-types/new/', views_crud.ClothingTypeCreateView.as_view(), name='clothing_type_create'),
    path('clothing-types/<int:pk>/', views_crud.ClothesTypeDetailView.as_view(), name='clothing_type_detail'),
    path('clothing-types/<int:pk>/edit/', views_crud.ClothingTypeUpdateView.as_view(), name='clothing_type_update'),
    path('clothing-types/<int:pk>/delete/', views_crud.ClothingTypeDeleteView.as_view(), name='clothing_type_delete'),
    
    # Альтернативные пути для ClothesType
    path('clothestypes/', views_crud.ClothesTypeListView.as_view(), name='clothestype_list'),
    path('clothestypes/new/', views_crud.ClothesTypeCreateView.as_view(), name='clothestype_create'),
    path('clothestypes/<int:pk>/', views_crud.ClothesTypeDetailView.as_view(), name='clothestype_detail'),
    path('clothestypes/<int:pk>/edit/', views_crud.ClothesTypeUpdateView.as_view(), name='clothestype_update'),
    path('clothestypes/<int:pk>/delete/', views_crud.ClothesTypeDeleteView.as_view(), name='clothestype_delete'),

    # CRUD для размеров
    path('sizes/', views_crud.SizeListView.as_view(), name='size_list'),
    path('sizes/new/', views_crud.SizeCreateView.as_view(), name='size_create'),
    path('sizes/<int:pk>/', views_crud.SizeDetailView.as_view(), name='size_detail'),
    path('sizes/<int:pk>/edit/', views_crud.SizeUpdateView.as_view(), name='size_update'),
    path('sizes/<int:pk>/delete/', views_crud.SizeDeleteView.as_view(), name='size_delete'),

    # CRUD для ассортимента
    path('assortment/', views_crud.AssortmentListView.as_view(), name='assortment_list'),
    path('assortment/new/', views_crud.AssortmentCreateView.as_view(), name='assortment_create'),
    path('assortment/<int:pk>/', views_crud.AssortmentDetailView.as_view(), name='assortment_detail'),
    path('assortment/<int:pk>/edit/', views_crud.AssortmentUpdateView.as_view(), name='assortment_update'),
    path('assortment/<int:pk>/delete/', views_crud.AssortmentDeleteView.as_view(), name='assortment_delete'),

    # CRUD для покупок
    path('purchases/', views_crud.PurchaseListView.as_view(), name='purchase_list'),
    path('purchases/new/', views_crud.PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchases/<int:pk>/', views_crud.PurchaseDetailView.as_view(), name='purchase_detail'),
    path('purchases/<int:pk>/edit/', views_crud.PurchaseUpdateView.as_view(), name='purchase_update'),
    path('purchases/<int:pk>/delete/', views_crud.PurchaseDeleteView.as_view(), name='purchase_delete'),

    # Аналитические страницы
    path('analytics/sales-stats/', views.sales_stats, name='sales_stats'),
    path('analytics/sales-by-customer/', views.sales_by_customer, name='sales_by_customer'),
    path('analytics/sales-by-type/', views.sales_by_type, name='sales_by_type'),
    path('analytics/assortment-by-size/', views.assortment_by_size, name='assortment_by_size'),
    path('analytics/seller-performance/', views.seller_performance, name='seller_performance'),
    path('analytics/daily-sales/', views.daily_sales_report, name='daily_sales'),
    path('analytics/customer-segments/', views.customer_segments, name='customer_segments'),
    path('analytics/inventory-status/', views.inventory_status, name='inventory_status'),
    path('analytics/top-products/', views.top_products, name='top_products'),
    path('analytics/purchase-trends/', views.purchase_trends, name='purchase_trends'),

    # ============================================================================
    # ЗАДАЧА 3: CRUD ДЛЯ POSTGRESQL МОДЕЛЕЙ
    # ============================================================================

    # CRUD для DeliveryMethod
    path('delivery-methods/', views_crud.DeliveryMethodListView.as_view(), name='delivery_method_list'),
    path('delivery-methods/new/', views_crud.DeliveryMethodCreateView.as_view(), name='delivery_method_create'),
    path('delivery-methods/<int:pk>/', views_crud.DeliveryMethodDetailView.as_view(), name='delivery_method_detail'),
    path('delivery-methods/<int:pk>/edit/', views_crud.DeliveryMethodUpdateView.as_view(), name='delivery_method_update'),
    path('delivery-methods/<int:pk>/delete/', views_crud.DeliveryMethodDeleteView.as_view(), name='delivery_method_delete'),

    # CRUD для BuyerProfile
    path('buyer-profiles/', views_crud.BuyerProfileListView.as_view(), name='buyer_profile_list'),
    path('buyer-profiles/new/', views_crud.BuyerProfileCreateView.as_view(), name='buyer_profile_create'),
    path('buyer-profiles/<int:pk>/', views_crud.BuyerProfileDetailView.as_view(), name='buyer_profile_detail'),
    path('buyer-profiles/<int:pk>/edit/', views_crud.BuyerProfileUpdateView.as_view(), name='buyer_profile_update'),
    path('buyer-profiles/<int:pk>/delete/', views_crud.BuyerProfileDeleteView.as_view(), name='buyer_profile_delete'),

    # CRUD для Order
    path('orders/', views_crud.OrderListView.as_view(), name='order_list'),
    path('orders/new/', views_crud.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', views_crud.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/edit/', views_crud.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views_crud.OrderDeleteView.as_view(), name='order_delete'),

    # CRUD для OrderItem
    path('order-items/new/', views_crud.OrderItemCreateView.as_view(), name='order_item_create'),
    path('order-items/<int:pk>/edit/', views_crud.OrderItemUpdateView.as_view(), name='order_item_update'),
    path('order-items/<int:pk>/delete/', views_crud.OrderItemDeleteView.as_view(), name='order_item_delete'),
]