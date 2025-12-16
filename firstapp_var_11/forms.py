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


# ============================================================================
# ЗАДАЧА 3: ФОРМЫ ДЛЯ POSTGRESQL МОДЕЛЕЙ
# ============================================================================

class DeliveryMethodForm(forms.ModelForm):
    """Форма для способа доставки"""
    class Meta:
        model = DeliveryMethod
        fields = ['name', 'description', 'cost', 'delivery_time_days', 'is_active', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название способа доставки'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'delivery_time_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '365'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'icon': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'cost': 'Стоимость доставки (руб.)',
            'delivery_time_days': 'Срок доставки (дней)',
            'is_active': 'Активен',
            'icon': 'Иконка',
        }


class BuyerProfileForm(forms.ModelForm):
    """Форма для профиля покупателя с валидацией"""
    class Meta:
        model = BuyerProfile
        fields = ['photo', 'passport_scan', 'address', 'birth_date', 'preferred_delivery_time', 'notes']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'passport_scan': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'preferred_delivery_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'photo': 'Фото покупателя',
            'passport_scan': 'Скан паспорта',
            'address': 'Адрес доставки',
            'birth_date': 'Дата рождения',
            'preferred_delivery_time': 'Предпочтительное время доставки',
            'notes': 'Дополнительные заметки',
        }

    def clean_birth_date(self):
        """Валидация даты рождения"""
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            from datetime import date
            if birth_date > date.today():
                raise forms.ValidationError('Дата рождения не может быть в будущем')
        return birth_date


class OrderForm(forms.ModelForm):
    """Форма для заказа с выбором из списков (POST метод)"""
    class Meta:
        model = Order
        fields = [
            'buyer', 'seller', 'delivery_method', 'order_number', 'delivery_date', 
            'delivery_time', 'status', 'total_amount', 'delivery_cost', 
            'discount_percent', 'delivery_address', 'contact_phone', 'notes',
            'invoice_file', 'delivery_confirmation_photo'
        ]
        widgets = {
            'buyer': forms.Select(attrs={'class': 'form-control'}),
            'seller': forms.Select(attrs={'class': 'form-control'}),
            'delivery_method': forms.Select(attrs={'class': 'form-control'}),
            'order_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'ORD-YYYY-NNNNNN',
                'pattern': 'ORD-\\d{4}-\\d{6}'
            }),
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'delivery_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'delivery_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+1234567890',
                'pattern': '\\+?1?\\d{9,15}'
            }),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'invoice_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'delivery_confirmation_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'buyer': 'Покупатель',
            'seller': 'Продавец',
            'delivery_method': 'Способ доставки',
            'order_number': 'Номер заказа',
            'delivery_date': 'Дата доставки',
            'delivery_time': 'Время доставки',
            'status': 'Статус заказа',
            'total_amount': 'Общая сумма заказа',
            'delivery_cost': 'Стоимость доставки',
            'discount_percent': 'Скидка (%)',
            'delivery_address': 'Адрес доставки',
            'contact_phone': 'Контактный телефон',
            'notes': 'Примечания',
            'invoice_file': 'Файл счета',
            'delivery_confirmation_photo': 'Фото подтверждения доставки',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем списки для выбора
        self.fields['buyer'].queryset = Buyer.objects.all().order_by('last_name', 'first_name')
        self.fields['seller'].queryset = Seller.objects.all().order_by('last_name', 'first_name')
        self.fields['delivery_method'].queryset = DeliveryMethod.objects.filter(is_active=True)

    def clean_order_number(self):
        """Валидация номера заказа"""
        order_number = self.cleaned_data.get('order_number')
        import re
        if not re.match(r'^ORD-\d{4}-\d{6}$', order_number):
            raise forms.ValidationError('Номер заказа должен быть в формате ORD-YYYY-NNNNNN')
        return order_number

    def clean_contact_phone(self):
        """Валидация телефона"""
        phone = self.cleaned_data.get('contact_phone')
        import re
        if not re.match(r'^\+?1?\d{9,15}$', phone):
            raise forms.ValidationError('Телефон должен быть в формате +1234567890')
        return phone

    def clean(self):
        """Валидация всей формы"""
        cleaned_data = super().clean()
        delivery_date = cleaned_data.get('delivery_date')
        order_date = self.instance.order_date if self.instance.pk else None
        
        if delivery_date and order_date:
            if delivery_date < order_date:
                raise forms.ValidationError({
                    'delivery_date': 'Дата доставки не может быть раньше даты заказа'
                })
        
        discount = cleaned_data.get('discount_percent', 0)
        if discount > 100:
            raise forms.ValidationError({
                'discount_percent': 'Скидка не может быть больше 100%'
            })
        
        return cleaned_data


class OrderItemForm(forms.ModelForm):
    """Форма для позиции заказа с выбором из списков"""
    class Meta:
        model = OrderItem
        fields = ['assortment', 'quantity', 'unit_price', 'discount_percent', 'size', 'notes']
        widgets = {
            'assortment': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'assortment': 'Товар',
            'quantity': 'Количество',
            'unit_price': 'Цена за единицу',
            'discount_percent': 'Скидка на позицию (%)',
            'size': 'Размер',
            'notes': 'Примечания',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем списки для выбора
        self.fields['assortment'].queryset = Assortment.objects.filter(stock_quantity__gt=0).order_by('name')
        self.fields['size'].queryset = Size.objects.all().order_by('size_value')

    def clean_quantity(self):
        """Валидация количества"""
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Количество должно быть больше 0')
        return quantity

    def clean(self):
        """Валидация позиции заказа"""
        cleaned_data = super().clean()
        assortment = cleaned_data.get('assortment')
        quantity = cleaned_data.get('quantity')
        
        if assortment and quantity:
            if assortment.stock_quantity < quantity:
                raise forms.ValidationError({
                    'quantity': f'Недостаточно товара на складе. Доступно: {assortment.stock_quantity}'
                })
        
        return cleaned_data


class OrderItemInlineFormSet(forms.BaseInlineFormSet):
    """FormSet для множественного добавления позиций заказа"""
    def clean(self):
        """Валидация всего formset"""
        if any(self.errors):
            return
        
        if not any(cleaned_data and not cleaned_data.get('DELETE', False) 
                   for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('Добавьте хотя бы одну позицию в заказ')