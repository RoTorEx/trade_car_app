from django.contrib import admin
from car.models import Car, CarPrice, CarCharacters


# Tuple of current application models
models = (Car, CarPrice, CarCharacters,)

# Registration of models
for m in models:
    admin.site.register(m)
