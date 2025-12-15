from django.db import models
from django.urls import reverse


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