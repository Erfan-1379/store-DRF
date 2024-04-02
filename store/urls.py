from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('carts', views.CartViewSet, basename='')
router.register('customers', views.CustomerVewSet, basename='customer')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comment')
cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart_items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(cart_items_router.urls)),
]
