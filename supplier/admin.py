from django.contrib import admin
from supplier.models import Supplier, SupplierGarage, SupplierPromo


# Tuple of current application models
models = (Supplier, SupplierGarage, SupplierPromo)

# Registration of models
for m in models:
    admin.site.register(m)
