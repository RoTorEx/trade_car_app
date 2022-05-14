from django.contrib import admin
from dealership.models import (
    Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory, DealershipPromo, DealerStatistic
)


# Tuple of current application models
models = (Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory, DealershipPromo, DealerStatistic)

# Registration of models
for m in models:
    admin.site.register(m)
