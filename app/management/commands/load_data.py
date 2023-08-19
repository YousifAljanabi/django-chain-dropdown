from django.core.management.base import BaseCommand
from app.models import Manufacturer, Car, CarModel


class Command(BaseCommand):
    help = 'Load data into database'

    def handle(self, *args, **options):
        Manufacturer.objects.all().delete()

        manufacturer_names = [
            'Audi', 'BMW', 'Mercedes-Benz'
        ]
        if not Manufacturer.objects.all().exists():
            for name in manufacturer_names:
                Manufacturer.objects.create(name=name)

        audi_cars = [
            'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'Q3', 'Q5', 'Q7', 'Q8', 'TT'
        ]
        bmw_cars = [
            'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'M3', 'M4', 'M5', 'M6'
        ]
        mercedes_cars = [
            'A-class', 'B-class', 'C-class', 'E-class', 'S-class', 'G-class', 'GLA', 'GLC', 'GLE', 'GLS', 'SLC'
        ]
        if not Car.objects.all().exists():
            for car in audi_cars:
                Car.objects.create(name=car, manufacturer=Manufacturer.objects.get(name='Audi'))
            for car in bmw_cars:
                Car.objects.create(name=car, manufacturer=Manufacturer.objects.get(name='BMW'))
            for car in mercedes_cars:
                Car.objects.create(name=car, manufacturer=Manufacturer.objects.get(name='Mercedes-Benz'))

        for car in Car.objects.all():
            if not CarModel.objects.filter(car=car).exists():
                for year in range(2010, 2022):
                    CarModel.objects.create(name=f'{car.name} {year}', car=car)
