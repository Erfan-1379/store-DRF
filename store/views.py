from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count() > 0:
            return Response({'error': 'There is some items including this product. please remove them first.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'There is some product relation this category. please remove them first.'})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk).all()

    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}
