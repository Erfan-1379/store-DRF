from _decimal import Decimal
from django.utils.text import slugify
from rest_framework import serializers

from .models import *

DOLLARS_TO_RIALS = 50000


class CategorySerializer(serializers.ModelSerializer):
    # nums_products = serializers.SerializerMethodField()
    nums_products = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'nums_products']

    # def get_nums_products(self, category):
    #     return category.products.count()


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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body']

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id, **validated_data)


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_pk']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)
        self.instance = cart_item
        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id']

    def get_total_price(self, cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())

