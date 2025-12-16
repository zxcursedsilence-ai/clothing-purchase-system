class PostgresRouter:
    """Маршрутизатор для моделей PostgreSQL"""

    def db_for_read(self, model, **hints):
        # #region agent log
        import json
        log_path = r'c:\Users\kiril\PycharmProjects\PythonProject_Kursovaya\.cursor\debug.log'
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'database_routers.py:5', 'message': 'db_for_read called', 'data': {'hypothesisId': 'B', 'model_name': model._meta.model_name}, 'timestamp': __import__('time').time() * 1000, 'sessionId': 'debug-session', 'runId': 'run1'}) + '\n')
        except: pass
        # #endregion
        
        # Модели для PostgreSQL (задачи 2.4 и 3)
        postgres_models = ['seller', 'sellerprofile', 'deliverymethod', 'buyerprofile', 'order', 'orderitem']
        if model._meta.model_name.lower() in postgres_models:
            # #region agent log
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({'location': 'database_routers.py:7', 'message': 'Routing to postgres', 'data': {'hypothesisId': 'B', 'model_name': model._meta.model_name}, 'timestamp': __import__('time').time() * 1000, 'sessionId': 'debug-session', 'runId': 'run1'}) + '\n')
            except: pass
            # #endregion
            return 'postgres'
        return None

    def db_for_write(self, model, **hints):
        # #region agent log
        import json
        log_path = r'c:\Users\kiril\PycharmProjects\PythonProject_Kursovaya\.cursor\debug.log'
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'database_routers.py:10', 'message': 'db_for_write called', 'data': {'hypothesisId': 'B', 'model_name': model._meta.model_name}, 'timestamp': __import__('time').time() * 1000, 'sessionId': 'debug-session', 'runId': 'run1'}) + '\n')
        except: pass
        # #endregion
        
        # Модели для PostgreSQL (задачи 2.4 и 3)
        postgres_models = ['seller', 'sellerprofile', 'deliverymethod', 'buyerprofile', 'order', 'orderitem']
        if model._meta.model_name.lower() in postgres_models:
            return 'postgres'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Разрешаем связи между моделями одной БД
        postgres_models = ['seller', 'sellerprofile', 'deliverymethod', 'buyerprofile', 'order', 'orderitem']
        db1 = 'postgres' if obj1._meta.model_name.lower() in postgres_models else 'default'
        db2 = 'postgres' if obj2._meta.model_name.lower() in postgres_models else 'default'
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        postgres_models = ['seller', 'sellerprofile', 'deliverymethod', 'buyerprofile', 'order', 'orderitem']
        if model_name and model_name.lower() in postgres_models:
            return db == 'postgres'
        # Для остальных моделей используем SQLite
        if db == 'postgres':
            return model_name and model_name.lower() in postgres_models
        return db == 'default'