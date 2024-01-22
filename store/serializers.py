from _decimal import Decimal
from django.utils.text import slugify
from rest_framework import serializers

from .models import *

DOLLARS_TO_RIALS = 50000


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500)


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, source='name')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    unit_price_after_tax = serializers.SerializerMethodField()
    price_rials = serializers.SerializerMethodField()
    category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(), view_name='category-detail')

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'inventory', 'category', 'unit_price_after_tax', 'price_rials']

    def get_unit_price_after_tax(self, product):
        return round(product.unit_price * Decimal(1.5), 2)

    def get_price_rials(self, product):
        return int(product.unit_price * DOLLARS_TO_RIALS)

    def validate(self, data):
        print(data)
        if len(data['name']) < 6:
            raise serializers.ValidationError('Length is must be at least 6')
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product

    # def update(self, instance, validated_data):
    #     instance.inventory = 1
    #     instance.save()
    #     return instance

