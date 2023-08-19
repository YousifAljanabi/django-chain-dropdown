from django.urls import reverse
from app.models import Manufacturer, Car
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Button
from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin


class ManufacturersForm(DynamicFormMixin, forms.Form):

    manufacturers = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
    )

    cars = DynamicField(
        forms.ModelChoiceField,
        queryset=lambda form: Car.objects.filter(manufacturer=form['manufacturers'].value()),
        initial=lambda form: Car.objects.filter(manufacturer=form['manufacturers'].value()).first(),
        required=False,


    )

    price = forms.IntegerField(
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('manufacturers', css_class='included',
                      **{'hx-get': reverse('index'), 'hx-target': '#form', 'hx-trigger': 'change',
                         'hx-swap': 'outerHTML'}),
                    ),
            Div(
                Field('cars', css_class='form-control',
                      **{'hx-get': reverse('index'), 'hx-target': '#form',
                         'hx-swap': 'outerHTML', 'hx-include': '.included'},
                      ),
                css_class='form-group'
            ),
            Div(
                Field('price'),

            ),
            Div(
                Button(
                    'submit', 'Submit', css_class='btn btn-primary',
                    **{'hx-post': reverse('submit'), 'hx-target': 'body', 'hx-swap': 'outerHTML'}

                )
            )

            )


