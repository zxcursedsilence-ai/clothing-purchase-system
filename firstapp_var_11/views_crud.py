from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import (
    DeliveryMethodForm, BuyerProfileForm, OrderForm, OrderItemForm
)


# ============================================================================
# ЗАДАЧА 2.1: CRUD для ClothesType (одна таблица)
# ============================================================================

class ClothesTypeListView(ListView):
    model = ClothesType
    template_name = 'crud/clothestype_list.html'
    context_object_name = 'clothestypes'
    paginate_by = 10


class ClothesTypeDetailView(DetailView):
    model = ClothesType
    template_name = 'crud/clothestype_detail.html'
    context_object_name = 'clothestype'


class ClothesTypeCreateView(CreateView):
    model = ClothesType
    template_name = 'crud/clothestype_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('clothestype_list')


class ClothesTypeUpdateView(UpdateView):
    model = ClothesType
    template_name = 'crud/clothestype_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('clothestype_list')


class ClothesTypeDeleteView(DeleteView):
    model = ClothesType
    template_name = 'crud/clothestype_confirm_delete.html'
    success_url = reverse_lazy('clothestype_list')


# ============================================================================
# ЗАДАЧА 2.2: CRUD для Buyer и Purchase (1:M)
# ============================================================================

class BuyerListView(ListView):
    model = Buyer
    template_name = 'crud/buyer_list.html'
    context_object_name = 'buyers'
    paginate_by = 15


class BuyerDetailView(DetailView):
    model = Buyer
    template_name = 'crud/buyer_detail.html'
    context_object_name = 'buyer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = self.object.purchases.all()
        return context


class BuyerCreateView(CreateView):
    model = Buyer
    template_name = 'crud/buyer_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'gender', 'is_vip']
    success_url = reverse_lazy('buyer_list')


class BuyerUpdateView(UpdateView):
    model = Buyer
    template_name = 'crud/buyer_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'gender', 'is_vip']
    success_url = reverse_lazy('buyer_list')


class BuyerDeleteView(DeleteView):
    model = Buyer
    template_name = 'crud/buyer_confirm_delete.html'
    success_url = reverse_lazy('buyer_list')


# Покупки (связь с Buyer)
class PurchaseCreateView(CreateView):
    model = Purchase
    template_name = 'crud/purchase_form.html'
    fields = ['buyer', 'total_amount', 'payment_method', 'notes']

    def get_success_url(self):
        return reverse_lazy('buyer_detail', args=[self.object.buyer.id])


class PurchaseUpdateView(UpdateView):
    model = Purchase
    template_name = 'crud/purchase_form.html'
    fields = ['total_amount', 'payment_method', 'notes']

    def get_success_url(self):
        return reverse_lazy('buyer_detail', args=[self.object.buyer.id])


class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = 'crud/purchase_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('buyer_detail', args=[self.object.buyer.id])


# ============================================================================
# ЗАДАЧА 2.3: CRUD для Assortment (M:M через Size)
# ============================================================================

class AssortmentListView(ListView):
    model = Assortment
    template_name = 'crud/assortment_list.html'
    context_object_name = 'assortments'
    paginate_by = 12


class AssortmentDetailView(DetailView):
    model = Assortment
    template_name = 'crud/assortment_detail.html'
    context_object_name = 'assortment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sizes_available'] = self.object.assortmentsize_set.all()
        return context


class AssortmentCreateView(CreateView):
    model = Assortment
    template_name = 'crud/assortment_form.html'
    fields = ['name', 'clothes_type', 'category', 'description', 'price', 'stock_quantity']
    success_url = reverse_lazy('assortment_list')


class AssortmentUpdateView(UpdateView):
    model = Assortment
    template_name = 'crud/assortment_form.html'
    fields = ['name', 'clothes_type', 'category', 'description', 'price', 'stock_quantity']
    success_url = reverse_lazy('assortment_list')


class AssortmentDeleteView(DeleteView):
    model = Assortment
    template_name = 'crud/assortment_confirm_delete.html'
    success_url = reverse_lazy('assortment_list')


# ============================================================================
# ЗАДАЧА 2.4: CRUD для Seller (1:1)
# ============================================================================

class SellerListView(ListView):
    model = Seller
    template_name = 'crud/seller_list.html'
    context_object_name = 'sellers'
    paginate_by = 10


class SellerDetailView(DetailView):
    model = Seller
    template_name = 'crud/seller_detail.html'
    context_object_name = 'seller'


class SellerCreateView(CreateView):
    model = Seller
    template_name = 'crud/seller_form.html'
    fields = ['first_name', 'last_name', 'email', 'hire_date']
    success_url = reverse_lazy('seller_list')


class SellerUpdateView(UpdateView):
    model = Seller
    template_name = 'crud/seller_form.html'
    fields = ['first_name', 'last_name', 'email', 'hire_date']
    success_url = reverse_lazy('seller_list')


class SellerDeleteView(DeleteView):
    model = Seller
    template_name = 'crud/seller_confirm_delete.html'
    success_url = reverse_lazy('seller_list')


# ============================================================================
# CRUD для Size (для задачи 2.3)
# ============================================================================

class SizeListView(ListView):
    model = Size
    template_name = 'crud/size_list.html'
    context_object_name = 'sizes'
    paginate_by = 15


class SizeDetailView(DetailView):
    model = Size
    template_name = 'crud/size_detail.html'
    context_object_name = 'size'


class SizeCreateView(CreateView):
    model = Size
    template_name = 'crud/size_form.html'
    fields = ['size_value', 'system', 'description']
    success_url = reverse_lazy('size_list')


class SizeUpdateView(UpdateView):
    model = Size
    template_name = 'crud/size_form.html'
    fields = ['size_value', 'system', 'description']
    success_url = reverse_lazy('size_list')


class SizeDeleteView(DeleteView):
    model = Size
    template_name = 'crud/size_confirm_delete.html'
    success_url = reverse_lazy('size_list')


# ============================================================================
# Дополнительные CRUD для Purchase (полный список и детали)
# ============================================================================

class PurchaseListView(ListView):
    model = Purchase
    template_name = 'crud/purchase_list.html'
    context_object_name = 'purchases'
    paginate_by = 20
    ordering = ['-purchase_date']


class PurchaseDetailView(DetailView):
    model = Purchase
    template_name = 'crud/purchase_detail.html'
    context_object_name = 'purchase'


# ============================================================================
# Алиасы для совместимости (Customer -> Buyer)
# ============================================================================

# Для совместимости с существующими ссылками
CustomerListView = BuyerListView
CustomerDetailView = BuyerDetailView
CustomerCreateView = BuyerCreateView
CustomerUpdateView = BuyerUpdateView
CustomerDeleteView = BuyerDeleteView

# Алиасы для ClothesType
ClothingTypeListView = ClothesTypeListView
ClothingTypeCreateView = ClothesTypeCreateView
ClothingTypeUpdateView = ClothesTypeUpdateView
ClothingTypeDeleteView = ClothesTypeDeleteView


# ============================================================================
# ЗАДАЧА 3: CRUD ДЛЯ POSTGRESQL МОДЕЛЕЙ
# ============================================================================

# DeliveryMethod CRUD
class DeliveryMethodListView(ListView):
    model = DeliveryMethod
    template_name = 'crud/deliverymethod_list.html'
    context_object_name = 'delivery_methods'
    paginate_by = 10


class DeliveryMethodDetailView(DetailView):
    model = DeliveryMethod
    template_name = 'crud/deliverymethod_detail.html'
    context_object_name = 'delivery_method'


class DeliveryMethodCreateView(CreateView):
    model = DeliveryMethod
    template_name = 'crud/deliverymethod_form.html'
    form_class = DeliveryMethodForm
    success_url = reverse_lazy('delivery_method_list')


class DeliveryMethodUpdateView(UpdateView):
    model = DeliveryMethod
    template_name = 'crud/deliverymethod_form.html'
    form_class = DeliveryMethodForm
    success_url = reverse_lazy('delivery_method_list')


class DeliveryMethodDeleteView(DeleteView):
    model = DeliveryMethod
    template_name = 'crud/deliverymethod_confirm_delete.html'
    success_url = reverse_lazy('delivery_method_list')


# BuyerProfile CRUD
class BuyerProfileListView(ListView):
    model = BuyerProfile
    template_name = 'crud/buyerprofile_list.html'
    context_object_name = 'profiles'
    paginate_by = 15


class BuyerProfileDetailView(DetailView):
    model = BuyerProfile
    template_name = 'crud/buyerprofile_detail.html'
    context_object_name = 'profile'


class BuyerProfileCreateView(CreateView):
    model = BuyerProfile
    template_name = 'crud/buyerprofile_form.html'
    form_class = BuyerProfileForm
    success_url = reverse_lazy('buyer_profile_list')


class BuyerProfileUpdateView(UpdateView):
    model = BuyerProfile
    template_name = 'crud/buyerprofile_form.html'
    form_class = BuyerProfileForm
    success_url = reverse_lazy('buyer_profile_list')


class BuyerProfileDeleteView(DeleteView):
    model = BuyerProfile
    template_name = 'crud/buyerprofile_confirm_delete.html'
    success_url = reverse_lazy('buyer_profile_list')


# Order CRUD
class OrderListView(ListView):
    model = Order
    template_name = 'crud/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    ordering = ['-order_date', '-order_time']


class OrderDetailView(DetailView):
    model = Order
    template_name = 'crud/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.order_items.all()
        return context


class OrderCreateView(CreateView):
    model = Order
    template_name = 'crud/order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_list')


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'crud/order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'crud/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


# OrderItem CRUD
class OrderItemCreateView(CreateView):
    model = OrderItem
    template_name = 'crud/orderitem_form.html'
    form_class = OrderItemForm
    
    def get_success_url(self):
        return reverse_lazy('order_detail', args=[self.object.order.id])


class OrderItemUpdateView(UpdateView):
    model = OrderItem
    template_name = 'crud/orderitem_form.html'
    form_class = OrderItemForm
    
    def get_success_url(self):
        return reverse_lazy('order_detail', args=[self.object.order.id])


class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = 'crud/orderitem_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('order_detail', args=[self.object.order.id])