from django.contrib import admin
from supplier.models import Supplier, SupplierHistory


# Tuple of current application models
models = (Supplier, SupplierHistory,)

# Registration of models
for m in models:
    admin.site.register(m)
