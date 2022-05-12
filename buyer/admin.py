from django.contrib import admin

from buyer.models import Buyer, BuyerHistory, BuyerOffer


# Tuple of current application models
models = (Buyer, BuyerHistory, BuyerOffer)

# Registration of models
for m in models:
    admin.site.register(m)
