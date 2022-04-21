from django.contrib import admin
from dealership.models import Dealership, DealershipHistory


# Tuple of current application models
models = (Dealership, DealershipHistory,)

# Registration of models
for m in models:
    admin.site.register(m)
