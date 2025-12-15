class PostgresRouter:
    """Маршрутизатор для моделей PostgreSQL"""

    def db_for_read(self, model, **hints):
        if model._meta.model_name in ['seller', 'sellerprofile']:
            return 'postgres'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name in ['seller', 'sellerprofile']:
            return 'postgres'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Разрешаем связи между моделями одной БД
        db1 = 'postgres' if obj1._meta.model_name in ['seller', 'sellerprofile'] else 'default'
        db2 = 'postgres' if obj2._meta.model_name in ['seller', 'sellerprofile'] else 'default'
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in ['seller', 'sellerprofile']:
            return db == 'postgres'
        return db == 'default'