"""
Основной URL конфигурация для проекта web_Hello_var_11.
Включает ВСЕ задачи: 1.1, 1.2, 1.3 и 2.1-2.4
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from firstapp_var_11 import views

urlpatterns = [
    # ============================================================================
    # АДМИНИСТРАТИВНЫЕ URL
    # ============================================================================
    path('admin/', admin.site.urls),

    # ============================================================================
    # ГЛАВНАЯ СТРАНИЦА (должна быть доступна без префикса приложения)
    # ============================================================================
    path('', views.index, name='index'),

    # ============================================================================
    # ЗАДАЧА 2: CRUD ОПЕРАЦИИ (включаются из приложения)
    # ============================================================================
    path('', include('firstapp_var_11.urls')),

    # ============================================================================
    # ОСНОВНЫЕ СТРАНИЦЫ
    # ============================================================================
    path('navigator/', TemplateView.as_view(template_name='navigator.html'), name='navigator'),

    # ============================================================================
    # ЗАДАЧА 1.1: ПРЕДСТАВЛЕНИЯ И МАРШРУТИЗАЦИЯ
    # ============================================================================

    # Основные страницы для навигатора
    path('buyers/', views.buyers, name='buyers'),
    path('clothes_type/', views.clothes_type, name='clothes_type'),
    path('assortment/', views.assortment, name='assortment'),
    path('sizes/', views.sizes, name='sizes'),
    path('sellers/', views.sellers, name='sellers'),
    path('purchases/', views.purchases, name='purchases'),

    # Параметры через path (обязательные и по умолчанию)
    path('buyer/<int:buyer_id>/', views.buyer_detail, name='buyer_detail'),
    path('clothes/', views.clothes_list, name='clothes_list_default'),
    path('clothes/<str:category>/', views.clothes_list, name='clothes_list'),
    path('search/', views.search_assortment, name='search'),
    path('old_purchases/', views.old_purchases_page, name='old_purchases'),

    # re_path с регулярными выражениями
    re_path(r'^purchases/year/(?P<year>[0-9]{4})/$', views.purchase_year, name='purchase_year'),
    re_path(r'^reports/month/(?P<month>[0-9]{2})/$', views.month_report, name='month_report'),

    # ============================================================================
    # ЗАДАЧА 1.2: ШАБЛОНЫ (TEMPLATES)
    # ============================================================================

    # Данные из файлов
    path('tablica/', views.show_tablica_data, name='tablica_data'),

    # Галерея изображений
    path('gallery/', views.assortment_gallery, name='gallery'),

    # Шаблоны с изображениями
    path('assortment_with_images/',
         TemplateView.as_view(template_name='assortment_with_images.html'),
         name='assortment_with_images'),

    # ============================================================================
    # ЗАДАЧА 1.3: ФОРМЫ (FORMS)
    # ============================================================================

    # Формы POST (создание данных)
    path('buyer-form/', views.buyer_form_view, name='buyer_form'),
    path('purchase-form/', views.purchase_form_view, name='purchase_form'),

    # Формы GET (поиск и фильтрация)
    path('clothes-search/', views.clothes_search_view, name='clothes_search'),

    # Страницы успешной обработки форм
    path('form_success/',
         TemplateView.as_view(template_name='form_success.html'),
         name='form_success'),
    path('search_result/',
         TemplateView.as_view(template_name='search_result.html'),
         name='search_result'),
    path('purchase_success/',
         TemplateView.as_view(template_name='purchase_success.html'),
         name='purchase_success'),


    # ============================================================================
    # ДОПОЛНИТЕЛЬНЫЕ СТРАНИЦЫ
    # ============================================================================

    # Страницы для демонстрации связей
    path('buyer_purchases/<int:buyer_id>/',
         views.buyer_purchases,
         name='buyer_purchases'),
    path('clothes_sizes/<int:clothes_id>/',
         views.clothes_sizes,
         name='clothes_sizes'),

    # Статические страницы для демонстрации
    path('about/',
         TemplateView.as_view(template_name='about.html'),
         name='about'),
    path('contact/',
         TemplateView.as_view(template_name='contact.html'),
         name='contact'),
]

# Обработчик для страницы 404
handler404 = 'firstapp_var_11.views.handler404'

# Обработчик для страницы 500
handler500 = 'firstapp_var_11.views.handler500'