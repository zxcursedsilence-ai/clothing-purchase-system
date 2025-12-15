from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *


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