from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('cat/<category>', views.ProductListView.as_view(), name='product-categories-list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product-brands-list'),
    path('color/<str:color>/', views.ProductListView.as_view(), name='product-colors-list'),
    path('product-favorite', views.AddProductFavorite.as_view(), name='product-favorite'),
    path('my-favorites/', views.MyFavoritesView.as_view(), name='my-favorites'),
    path('detail/<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('preview/<int:product_id>/', views.template_preview, name='template_preview'),
    path('product-order/', views.AddProductOrder.as_view(), name='product-order'),
    path('my-orders/', views.MyOrdersView.as_view(), name='my-orders'),
    path('proforma/<int:proforma_id>/', views.ProformaDetailView.as_view(), name='proforma-detail'),
    path('finalize-payment/', views.FinalizePaymentView.as_view(), name='finalize-payment'),
    path('support/', views.ProductSupportView.as_view(), name='support'),



]
