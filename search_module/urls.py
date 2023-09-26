from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('result/', views.product_search, name='search-result'),
]
