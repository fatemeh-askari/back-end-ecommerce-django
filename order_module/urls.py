from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/', views.add_product_to_cart, name='add-to-cart'),
    path('remove-from-cart/', views.remove_product_from_cart, name='remove-product-from-cart'),
    path('list-cart/', views.order_list, name='list-cart'),
    path('remove-order/', views.remove_product_from_cart, name="remove-order")
]