from django_filters.rest_framework import FilterSet
from .models import *


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'inventory': ['lt', 'gt'],
        }
