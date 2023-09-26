from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('cat/<category>', views.ArticleListView.as_view(), name='article-categories-list'),
    path('detail/<slug:slug>', views.ArticleDetailView.as_view(), name='article-detail'),
]