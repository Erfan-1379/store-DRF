from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')


products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
