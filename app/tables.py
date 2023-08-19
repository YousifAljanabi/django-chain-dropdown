from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldDoesNotExist
from django.db.models import ManyToManyField
from django_tables2 import columns
from django.db.models.fields.related import RelatedField
from django_tables2 import Table, tables
from django_tables2.data import TableQuerysetData
from app.models import CarCombined



class BaseTable(Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(self.data, TableQuerysetData):

            prefetch_fields = []
            select_related_fields = []
            for column in self.columns:
                if column.visible:
                    model = getattr(self.Meta, 'model')
                    accessor = column.accessor
                    prefetch_path = []
                    select_related_path = []
                    for field_name in accessor.split(accessor.SEPARATOR):
                        try:
                            field = model._meta.get_field(field_name)
                        except FieldDoesNotExist:
                            break
                        if isinstance(field, RelatedField):
                            # Follow ForeignKeys to the related model
                            select_related_path.append(field_name)
                            model = field.remote_field.model
                        elif isinstance(field, ManyToManyField):
                            prefetch_path.append(field_name)
                            model = field.remote_field.model
                        elif isinstance(field, GenericForeignKey):
                            # Can't prefetch beyond a GenericForeignKey
                            prefetch_path.append(field_name)
                            break
                    if prefetch_path:
                        prefetch_fields.append('__'.join(prefetch_path))
                    if select_related_path:
                        select_related_fields.append('__'.join(select_related_path))
            self.data.data = self.data.data.select_related(*select_related_fields).prefetch_related(*prefetch_fields)


class CarsTable(BaseTable):
    manufacturer = columns.Column(verbose_name='Manufacturer')
    car = columns.Column(verbose_name='Car')
    price = columns.Column(verbose_name='Price')

    class Meta:
        model = CarCombined
        fields = ('manufacturer', 'car', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



