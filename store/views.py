from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *


@api_view()
def product_list(request):
    products_queryset = Product.objects.select_related('category').all()
    serializer = ProductSerializer(products_queryset, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def product_detail(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        # try:
        #     product = Product.objects.get(pk=id)
        # except Product.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('All Ok!')
        # if serializer.is_valid():
        #     serializer.validated_data()
        #     return Response('All Ok!')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response('OK')


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
