from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} {self.id}'


class Car(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='cars')

    def __str__(self):
        return f'{self.name} {self.id}'


class CarModel(models.Model):
    name = models.CharField(max_length=100)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='models')

    def __str__(self):
        return self.name


class CarCombined(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='cars_combined')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='models_combined')
    price = models.IntegerField()

    def __str__(self):
        return f'{self.manufacturer.name} {self.car.name} {self.price}'