from django.contrib import admin
from supplier.models import Supplier, SupplierGarage, SupplierPromo, SupplierStatistic


# Tuple of current application models
models = (Supplier, SupplierGarage, SupplierPromo, SupplierStatistic)

# Registration of models
for m in models:
    admin.site.register(m)
