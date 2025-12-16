import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from firstapp_var_11.models import (
    ClothesType, Size, Assortment, Buyer, Seller,
    DeliveryMethod, BuyerProfile, Order, OrderItem
)


class Command(BaseCommand):
    help = "Заполняет базу примерами данных для демонстрации сайта (SQLite + PostgreSQL)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=== Создание примерных данных по теме 'Покупка одежды' ==="))

        # --- Типы одежды ---
        clothes_types_data = [
            ("Платья", "Вечерние, повседневные и офисные платья"),
            ("Брюки", "Джинсы, классические брюки, чиносы"),
            ("Рубашки", "Мужские и женские рубашки"),
            ("Куртки", "Кожаные, демисезонные, зимние куртки"),
            ("Юбки", "Юбки разных фасонов и длины"),
            ("Футболки", "Базовые и принтованные футболки"),
        ]
        clothes_types = []
        for name, desc in clothes_types_data:
            obj, _ = ClothesType.objects.get_or_create(name=name, defaults={"description": desc})
            clothes_types.append(obj)
        self.stdout.write(self.style.SUCCESS(f"Типы одежды: {len(clothes_types)} шт."))

        # --- Размеры ---
        size_values_int = ["XS", "S", "M", "L", "XL"]
        sizes = []
        for val in size_values_int:
            obj, _ = Size.objects.get_or_create(size_value=val, system="int", defaults={"description": f"Размер {val}"})
            sizes.append(obj)
        self.stdout.write(self.style.SUCCESS(f"Размеры: {len(sizes)} шт."))

        # --- Ассортимент ---
        assortments_data = [
            ("Платье вечернее синее", "Платья", "dress", 4500),
            ("Платье повседневное бежевое", "Платья", "dress", 3200),
            ("Джинсы скинни синие", "Брюки", "bottom", 2800),
            ("Брюки классические чёрные", "Брюки", "bottom", 3500),
            ("Рубашка белая классическая", "Рубашки", "top", 2200),
            ("Рубашка в клетку", "Рубашки", "top", 2400),
            ("Куртка кожаная", "Куртки", "top", 8900),
            ("Куртка джинсовая", "Куртки", "top", 6100),
            ("Юбка карандаш", "Юбки", "dress", 2700),
            ("Футболка базовая белая", "Футболки", "underwear", 1200),
            ("Футболка с принтом", "Футболки", "underwear", 1500),
        ]
        assortments = []
        for name, type_name, category, price in assortments_data:
            ct = next(ct for ct in clothes_types if ct.name == type_name)
            obj, _ = Assortment.objects.get_or_create(
                name=name,
                defaults={
                    "clothes_type": ct,
                    "category": category,
                    "description": name,
                    "price": price,
                    "stock_quantity": random.randint(5, 40),
                },
            )
            # Привязываем размеры через M2M
            obj.available_sizes.set(random.sample(sizes, k=min(3, len(sizes))))
            assortments.append(obj)
        self.stdout.write(self.style.SUCCESS(f"Ассортимент: {len(assortments)} товаров"))

        # --- Покупатели ---
        buyers_data = [
            ("Иван", "Иванов", "ivanov@example.com", "M"),
            ("Мария", "Петрова", "petrova@example.com", "F"),
            ("Алексей", "Сидоров", "sidorov@example.com", "M"),
            ("Анна", "Кузнецова", "kuznetsova@example.com", "F"),
            ("Дмитрий", "Смирнов", "smirnov@example.com", "M"),
        ]
        buyers = []
        for first, last, email, gender in buyers_data:
            obj, _ = Buyer.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "gender": gender,
                    "phone": "+7999000000",
                    "is_vip": random.choice([True, False]),
                },
            )
            buyers.append(obj)
        self.stdout.write(self.style.SUCCESS(f"Покупатели: {len(buyers)} шт."))

        # --- Продавцы (PostgreSQL) ---
        sellers_data = [
            ("Ольга", "Менеджер", "olga.manager@example.com"),
            ("Сергей", "Продавец", "sergey.seller@example.com"),
        ]
        sellers = []
        for first, last, email in sellers_data:
            obj, _ = Seller.objects.using("postgres").get_or_create(
                email=email,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "hire_date": date.today() - timedelta(days=random.randint(100, 2000)),
                },
            )
            sellers.append(obj)
        self.stdout.write(self.style.SUCCESS(f"Продавцы (PostgreSQL): {len(sellers)} шт."))

        # --- Способы доставки (PostgreSQL) ---
        delivery_data = [
            ("Курьер по городу", "Доставка курьером в пределах города", 350, 2),
            ("Пункт выдачи", "Самовывоз из пункта выдачи", 150, 3),
            ("Почта России", "Доставка в регионы России", 400, 7),
        ]
        methods = []
        for name, desc, cost, days in delivery_data:
            obj, _ = DeliveryMethod.objects.using("postgres").get_or_create(
                name=name,
                defaults={
                    "description": desc,
                    "cost": cost,
                    "delivery_time_days": days,
                    "is_active": True,
                },
            )
            methods.append(obj)
        self.stdout.write(self.style.SUCCESS(f"Способы доставки (PostgreSQL): {len(methods)} шт."))

        # --- Профили покупателей (PostgreSQL 1:1) ---
        for buyer in buyers:
            BuyerProfile.objects.using("postgres").get_or_create(
                buyer=buyer,
                defaults={
                    "address": "г. Минск, пр-т Победителей, д. 1",
                    "notes": "Профиль создан автоматически для демо.",
                },
            )
        self.stdout.write(self.style.SUCCESS("Профили покупателей (PostgreSQL) созданы"))

        # --- Заказы и позиции (PostgreSQL) ---
        today = timezone.now().date()
        for i in range(1, 6):
            buyer = random.choice(buyers)
            seller = random.choice(sellers)
            method = random.choice(methods)
            order_date = today - timedelta(days=random.randint(0, 10))
            order_number = f"ORD-{order_date.year}-{i:06d}"

            order, created = Order.objects.using("postgres").get_or_create(
                order_number=order_number,
                defaults={
                    "buyer": buyer,
                    "seller": seller,
                    "delivery_method": method,
                    "order_date": order_date,
                    "order_time": timezone.now().time(),
                    "delivery_date": order_date + timedelta(days=method.delivery_time_days),
                    "delivery_time": (timezone.now() + timedelta(hours=2)).time(),
                    "status": random.choice([s[0] for s in Order.STATUS_CHOICES]),
                    "total_amount": 0,
                    "delivery_cost": method.cost,
                    "discount_percent": random.choice([0, 5, 10, 15]),
                    "delivery_address": "г. Минск, ул. Ленина, д. 10",
                    "contact_phone": "+375291234567",
                },
            )

            # Позиции заказа
            if created:
                items_count = random.randint(1, 4)
                total_amount = 0
                for _ in range(items_count):
                    assortment = random.choice(assortments)
                    quantity = random.randint(1, 3)
                    unit_price = assortment.price
                    discount = random.choice([0, 5, 10])
                    size = random.choice(sizes)

                    item = OrderItem.objects.using("postgres").create(
                        order=order,
                        assortment=assortment,
                        quantity=quantity,
                        unit_price=unit_price,
                        discount_percent=discount,
                        size=size,
                    )
                    total_amount += item.get_subtotal()

                order.total_amount = total_amount
                order.save(using="postgres")

        self.stdout.write(self.style.SUCCESS("Заказы и позиции заказов (PostgreSQL) созданы"))
        self.stdout.write(self.style.SUCCESS("=== Демоданные успешно добавлены ==="))


