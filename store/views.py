from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *


class ProductList(APIView):
    def get(self, request):
        products_queryset = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products_queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count() > 0:
            return Response({'error': 'There is some items including this product. please remove them first.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    def get(self, request):
        categories_queryset = Category.objects.prefetch_related('products').all()
        # categories_queryset = Category.objects.annotate(products_count=Count('products')).all()
        serializer = CategorySerializer(categories_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetail(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def pus(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'There is some product relation this category. please remove them first.'})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
