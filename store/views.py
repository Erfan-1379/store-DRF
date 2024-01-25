from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products_queryset = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products_queryset, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    if request.method == "GET":
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if product.order_items.count() > 0:
            return Response({'error': 'There is some items including this product. please remove them first.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        # categories_queryset = Category.objects.prefetch_related('products').all()
        categories_queryset = Category.objects.annotate(products_count=Count('products')).all()
        serializer = CategorySerializer(categories_queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(Category.objects.annotate(products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if category.products.count() > 0:
            return Response({'error': 'There is some product relation this category. please remove them first.'})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
