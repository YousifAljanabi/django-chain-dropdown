from django.contrib import admin
from app.models import Manufacturer, Car, CarModel, CarCombined

admin.site.register(Manufacturer)
admin.site.register(Car)
admin.site.register(CarModel)
admin.site.register(CarCombined)
