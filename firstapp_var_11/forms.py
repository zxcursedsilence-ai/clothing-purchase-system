from django import forms
from .models import *

# Простая форма для добавления покупателя
class BuyerForm(forms.Form):
    name = forms.CharField(
        label='ФИО покупателя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    city = forms.CharField(
        label='Город',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    registration_date = forms.DateField(
        label='Дата регистрации',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )


# Форма с выбором из списка (одиночный выбор)
class ClothesSearchForm(forms.Form):
    CLOTHES_TYPES = [
        ('dress', 'Платья'),
        ('pants', 'Брюки'),
        ('shirt', 'Рубашки'),
        ('jacket', 'Куртки'),
        ('shoes', 'Обувь'),
    ]

    clothes_type = forms.ChoiceField(
        label='Тип одежды',
        choices=CLOTHES_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    SIZE_CHOICES = [
        ('S', 'S (Small)'),
        ('M', 'M (Medium)'),
        ('L', 'L (Large)'),
        ('XL', 'XL (Extra Large)'),
    ]

    size = forms.MultipleChoiceField(
        label='Размеры (можно выбрать несколько)',
        choices=SIZE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    min_price = forms.IntegerField(
        label='Минимальная цена',
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    max_price = forms.IntegerField(
        label='Максимальная цена',
        min_value=0,
        initial=10000,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


# Форма для добавления покупки
class PurchaseForm(forms.Form):
    buyer_name = forms.CharField(label='Имя покупателя', max_length=100)
    item_name = forms.CharField(label='Наименование товара', max_length=100)
    quantity = forms.IntegerField(label='Количество', min_value=1)
    purchase_date = forms.DateField(
        label='Дата покупки',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

# Форма для добавления размеров к ассортименту (M:M связь)
class AssortmentSizeForm(forms.ModelForm):
    class Meta:
        model = AssortmentSize
        fields = ['assortment', 'size', 'quantity']
        widgets = {
            'assortment': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Форма для поиска
class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск...'
        })
    )

# Форма для фильтрации
class FilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'Все категории')] + Assortment.CATEGORIES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )