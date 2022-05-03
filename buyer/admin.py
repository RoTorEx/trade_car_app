from django.contrib import admin

from buyer.models import Buyer, BuyerHistory


# Tuple of current application models
models = (Buyer, BuyerHistory)

# Registration of models
for m in models:
    admin.site.register(m)
