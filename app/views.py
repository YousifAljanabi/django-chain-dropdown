from django.shortcuts import render
from app.models import Manufacturer, Car, CarCombined
from app.forms import ManufacturersForm
from app.tables import CarsTable


def index(request):
    objs = CarCombined.objects.all()
    table = CarsTable(objs)
    if request.htmx:
        form = ManufacturersForm(request.GET)
        print(form['manufacturers'].value())
        print(form['cars'].value())
        return render(request, 'app/forms/form.html', {
            'form': form,
            'table': table,
        })

    form = ManufacturersForm()

    return render(request, 'app/list_cars.html', {
        'table': table,
        'form': form,
    })


def submit(request):
    if request.htmx:
        form = ManufacturersForm(request.POST)
        print(form['manufacturers'].value())
        manufacturer = Manufacturer.objects.get(id=form['manufacturers'].value())
        car = Car.objects.get(id=form['cars'].value())
        instance = CarCombined.objects.create(
            manufacturer=manufacturer,
            car=car,
            price=form['price'].value(),
        )
        print(instance)
        objs = CarCombined.objects.all()
        table = CarsTable(objs)
        form = ManufacturersForm()
        return render(request, 'app/list_cars.html', {
            'form': form,
            'table': table,
        })


