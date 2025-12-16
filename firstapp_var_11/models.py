from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
import os


# ============================================================================
# ЗАДАЧА 2.1: ОДНА ТАБЛИЦА (без связей)
# ============================================================================

class ClothesType(models.Model):
    """Тип одежды - для задачи 2.1 (одиночная таблица)"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название типа',
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Тип одежды'
        verbose_name_plural = 'Типы одежды'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clothestype_detail', args=[str(self.id)])


# ============================================================================
# ЗАДАЧА 2.2: ДВЕ ТАБЛИЦЫ (1 ко многим)
# ============================================================================

class Buyer(models.Model):
    """Покупатель - основная таблица для связи 1:M"""
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    ]

    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        blank=True
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Пол',
        default='O'
    )
    registration_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )
    is_vip = models.BooleanField(
        default=False,
        verbose_name='VIP клиент'
    )

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse('buyer_detail', args=[str(self.id)])

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"


class Purchase(models.Model):
    """Покупка - зависимая таблица (связь 1:M с Buyer)"""
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
        ('online', 'Онлайн оплата'),
    ]

    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,  # При удалении покупателя удаляются его покупки
        related_name='purchases',
        verbose_name='Покупатель'
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата покупки'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма покупки'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name='Способ оплаты',
        default='card'
    )
    notes = models.TextField(
        verbose_name='Примечания',
        blank=True
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-purchase_date']

    def __str__(self):
        return f"Покупка #{self.id} - {self.buyer.get_full_name()}"

    def get_absolute_url(self):
        return reverse('purchase_detail', args=[str(self.id)])


# ============================================================================
# ЗАДАЧА 2.3: ТРИ ТАБЛИЦЫ (M:M через промежуточную)
# ============================================================================

class Size(models.Model):
    """Размеры одежды"""
    SIZE_SYSTEMS = [
        ('int', 'Международный (XS-XXL)'),
        ('ru', 'Российский (42-56)'),
        ('eu', 'Европейский (36-50)'),
        ('us', 'Американский (2-20)'),
    ]

    size_value = models.CharField(
        max_length=10,
        verbose_name='Значение размера'
    )
    system = models.CharField(
        max_length=3,
        choices=SIZE_SYSTEMS,
        verbose_name='Система размеров',
        default='int'
    )
    description = models.CharField(
        max_length=100,
        verbose_name='Описание',
        blank=True
    )

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        unique_together = ['size_value', 'system']

    def __str__(self):
        return f"{self.size_value} ({self.get_system_display()})"


class Assortment(models.Model):
    """Ассортимент одежды"""
    CATEGORIES = [
        ('top', 'Верхняя одежда'),
        ('bottom', 'Нижняя одежда'),
        ('dress', 'Платья и юбки'),
        ('underwear', 'Белье'),
        ('accessories', 'Аксессуары'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Наименование товара'
    )
    clothes_type = models.ForeignKey(
        ClothesType,
        on_delete=models.PROTECT,  # Нельзя удалить тип, если есть товары этого типа
        related_name='assortments',
        verbose_name='Тип одежды'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        verbose_name='Категория'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    available_sizes = models.ManyToManyField(
        Size,
        through='AssortmentSize',  # Явное указание промежуточной таблицы
        verbose_name='Доступные размеры'
    )
    stock_quantity = models.IntegerField(
        verbose_name='Количество на складе',
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Ассортимент'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    def is_available(self):
        return self.stock_quantity > 0

    def get_absolute_url(self):
        return reverse('assortment_detail', args=[str(self.id)])


class AssortmentSize(models.Model):
    """Промежуточная таблица для связи M:M с дополнительными полями"""
    assortment = models.ForeignKey(
        Assortment,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        verbose_name='Размер'
    )
    quantity = models.IntegerField(
        verbose_name='Количество в наличии',
        default=0
    )

    class Meta:
        verbose_name = 'Наличие по размеру'
        verbose_name_plural = 'Наличие по размерам'
        unique_together = ['assortment', 'size']

    def __str__(self):
        return f"{self.assortment.name} - {self.size} ({self.quantity} шт.)"


# ============================================================================
# ЗАДАЧА 2.4: ДВЕ ТАБЛИЦЫ (1 к 1) - для PostgreSQL
# ============================================================================

class Seller(models.Model):
    """Продавец - основная таблица"""
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )
    hire_date = models.DateField(
        verbose_name='Дата найма'
    )

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse('seller_detail', args=[str(self.id)])


class SellerProfile(models.Model):
    """Профиль продавца - связь 1:1"""
    seller = models.OneToOneField(
        Seller,
        on_delete=models.CASCADE,
        primary_key=True,  # Важно для связи 1:1!
        related_name='profile',
        verbose_name='Продавец'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
    )
    address = models.TextField(
        verbose_name='Адрес'
    )
    birth_date = models.DateField(
        verbose_name='Дата рождения'
    )
    experience_years = models.IntegerField(
        verbose_name='Стаж (лет)',
        default=0
    )
    department = models.CharField(
        max_length=100,
        verbose_name='Отдел'
    )

    class Meta:
        verbose_name = 'Профиль продавца'
        verbose_name_plural = 'Профили продавцов'

    def __str__(self):
        return f"Профиль: {self.seller}"


# ============================================================================
# ЗАДАЧА 3: МОДЕЛИ ДЛЯ POSTGRESQL (3-5 таблиц с промежуточной таблицей)
# ============================================================================

class DeliveryMethod(models.Model):
    """Справочник способов доставки"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название способа доставки',
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость доставки',
        default=0,
        validators=[MinValueValidator(0)]
    )
    delivery_time_days = models.IntegerField(
        verbose_name='Срок доставки (дней)',
        validators=[MinValueValidator(1), MaxValueValidator(365)]
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    icon = models.ImageField(
        upload_to='delivery_icons/',
        verbose_name='Иконка',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'
        ordering = ['name']
        db_table = 'delivery_methods'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('delivery_method_detail', args=[str(self.id)])


class BuyerProfile(models.Model):
    """Расширенный профиль покупателя - связь 1:1 с Buyer"""
    buyer = models.OneToOneField(
        Buyer,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='buyer_profile',
        verbose_name='Покупатель'
    )
    photo = models.ImageField(
        upload_to='buyer_photos/',
        verbose_name='Фото покупателя',
        blank=True,
        null=True,
        help_text='Загрузите фото покупателя'
    )
    passport_scan = models.FileField(
        upload_to='buyer_documents/',
        verbose_name='Скан паспорта',
        blank=True,
        null=True,
        help_text='PDF или изображение паспорта'
    )
    address = models.TextField(
        verbose_name='Адрес доставки',
        blank=True
    )
    birth_date = models.DateField(
        verbose_name='Дата рождения',
        blank=True,
        null=True
    )
    preferred_delivery_time = models.TimeField(
        verbose_name='Предпочтительное время доставки',
        blank=True,
        null=True,
        help_text='Время, когда удобно получать заказы'
    )
    notes = models.TextField(
        verbose_name='Дополнительные заметки',
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания профиля'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Профиль покупателя'
        verbose_name_plural = 'Профили покупателей'
        db_table = 'buyer_profiles'

    def __str__(self):
        return f"Профиль: {self.buyer.get_full_name()}"

    def clean(self):
        """Валидация данных"""
        if self.birth_date:
            from datetime import date
            if self.birth_date > date.today():
                raise ValidationError({'birth_date': 'Дата рождения не может быть в будущем'})

    def get_absolute_url(self):
        return reverse('buyer_profile_detail', args=[str(self.buyer.id)])


class Order(models.Model):
    """Заказ - главная (промежуточная) таблица с связями M:1"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    # Связи M:1 к справочникам
    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.PROTECT,  # Нельзя удалить покупателя с заказами
        related_name='orders',
        verbose_name='Покупатель'
    )
    seller = models.ForeignKey(
        Seller,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Продавец',
        blank=True,
        null=True
    )
    delivery_method = models.ForeignKey(
        DeliveryMethod,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Способ доставки'
    )

    # Основные поля
    order_number = models.CharField(
        max_length=20,
        verbose_name='Номер заказа',
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^ORD-\d{4}-\d{6}$',
                message='Номер заказа должен быть в формате ORD-YYYY-NNNNNN'
            )
        ]
    )
    order_date = models.DateField(
        verbose_name='Дата заказа',
        auto_now_add=True
    )
    order_time = models.TimeField(
        verbose_name='Время заказа',
        auto_now_add=True
    )
    delivery_date = models.DateField(
        verbose_name='Дата доставки',
        blank=True,
        null=True
    )
    delivery_time = models.TimeField(
        verbose_name='Время доставки',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name='Статус заказа',
        default='pending'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Общая сумма заказа',
        validators=[MinValueValidator(0)]
    )
    delivery_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость доставки',
        default=0,
        validators=[MinValueValidator(0)]
    )
    discount_percent = models.IntegerField(
        verbose_name='Скидка (%)',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Дополнительные поля
    delivery_address = models.TextField(
        verbose_name='Адрес доставки'
    )
    contact_phone = models.CharField(
        max_length=20,
        verbose_name='Контактный телефон',
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Телефон должен быть в формате +1234567890'
            )
        ]
    )
    notes = models.TextField(
        verbose_name='Примечания к заказу',
        blank=True
    )
    
    # Файлы и изображения
    invoice_file = models.FileField(
        upload_to='order_invoices/',
        verbose_name='Файл счета',
        blank=True,
        null=True
    )
    delivery_confirmation_photo = models.ImageField(
        upload_to='delivery_confirmations/',
        verbose_name='Фото подтверждения доставки',
        blank=True,
        null=True
    )

    # Связь M:M с Assortment через OrderItem
    items = models.ManyToManyField(
        Assortment,
        through='OrderItem',
        related_name='orders',
        verbose_name='Товары в заказе'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date', '-order_time']
        db_table = 'orders'

    def __str__(self):
        return f"Заказ {self.order_number} - {self.buyer.get_full_name()}"

    def clean(self):
        """Валидация данных заказа"""
        if self.delivery_date and self.order_date:
            if self.delivery_date < self.order_date:
                raise ValidationError({
                    'delivery_date': 'Дата доставки не может быть раньше даты заказа'
                })
        
        if self.discount_percent > 100:
            raise ValidationError({
                'discount_percent': 'Скидка не может быть больше 100%'
            })

    def get_total_with_discount(self):
        """Расчет итоговой суммы со скидкой"""
        discount_amount = (self.total_amount * self.discount_percent) / 100
        return self.total_amount - discount_amount + self.delivery_cost

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])


class OrderItem(models.Model):
    """Промежуточная таблица для связи M:M между Order и Assortment"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Заказ'
    )
    assortment = models.ForeignKey(
        Assortment,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Товар'
    )
    quantity = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за единицу',
        validators=[MinValueValidator(0)]
    )
    discount_percent = models.IntegerField(
        verbose_name='Скидка на позицию (%)',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.PROTECT,
        verbose_name='Размер',
        blank=True,
        null=True
    )
    notes = models.TextField(
        verbose_name='Примечания к позиции',
        blank=True
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
        unique_together = ['order', 'assortment', 'size']
        db_table = 'order_items'

    def __str__(self):
        return f"{self.order.order_number} - {self.assortment.name} x{self.quantity}"

    def get_subtotal(self):
        """Расчет подытога по позиции"""
        subtotal = self.unit_price * self.quantity
        discount_amount = (subtotal * self.discount_percent) / 100
        return subtotal - discount_amount

    def clean(self):
        """Валидация позиции заказа"""
        if self.quantity <= 0:
            raise ValidationError({
                'quantity': 'Количество должно быть больше 0'
            })
        
        if self.unit_price < 0:
            raise ValidationError({
                'unit_price': 'Цена не может быть отрицательной'
            })
        
        # Проверка наличия товара на складе
        if self.assortment.stock_quantity < self.quantity:
            raise ValidationError({
                'quantity': f'Недостаточно товара на складе. Доступно: {self.assortment.stock_quantity}'
            })