from django.contrib import admin
from .models import Category, Discount, Product, Customer, Address, Order, OrderItem, Comment, Cart, CartItem
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'top_product']
    search_fields = ['title']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discount', 'description']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'unit_price', 'inventory', 'datetime_created', 'datetime_modified']
    list_filter = ['category', 'discounts']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'birth_date']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone_number']

    def first_name(self, customer):
        return customer.user.first_name

    def last_name(self, customer):
        return customer.user.last_name

    def email(self, customer):
        return customer.user.email


class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'province', 'city', 'street']
    list_filter = ['province', 'city']
    search_fields = ['street']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'datetime_created', 'status']
    list_filter = ['status']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__email']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    list_filter = ['order', 'product']
    search_fields = ['order__customer__first_name', 'order__customer__last_name', 'order__customer__email',
                     'product__name', 'product__slug']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'body', 'datetime_created', 'status']
    list_filter = ['product', 'status']
    search_fields = ['name', 'body']


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    fields = ['id', 'product', 'quantity']
    extra = 0
    min_num = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    inlines = [CartItemInline]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    list_filter = ['cart', 'product']
    search_fields = ['product__name', 'product__slug']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)