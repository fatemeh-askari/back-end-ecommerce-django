from django.urls import path
from . import views
from .views import HomeCategoryListView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('about-us', views.AboutView.as_view(), name='about_page'),
    path('products/cat/<category>/', HomeCategoryListView.as_view(), name='product-list-by-category'),


]
