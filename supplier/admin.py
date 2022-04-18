from django.contrib import admin
from .models import *


# Кортеж моделей текущего приложения
models = (Supplier, SupplierHistory,)

# Регистрация моделей
for m in models:
    admin.site.register(m)
