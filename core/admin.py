from django.contrib import admin
from core.models import Offer, Promotion


# Tuple of current application models
models = (Offer, Promotion,)

# Registration of models
for m in models:
    admin.site.register(m)
