from django.contrib import admin

from buyer.models import Buyer, BuyerHistory, BuyerOffer, BuyerStatistic


# Tuple of current application models
models = (Buyer, BuyerHistory, BuyerOffer, BuyerStatistic)

# Registration of models
for m in models:
    admin.site.register(m)
