from django.contrib import admin
from dealership.models import Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory, DealershipPromo


# Tuple of current application models
models = (Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory, DealershipPromo)

# Registration of models
for m in models:
    admin.site.register(m)
