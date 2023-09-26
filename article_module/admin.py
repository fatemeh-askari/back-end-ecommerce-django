from django.contrib import admin
from . import models

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ['category', 'is_active', 'author']
    list_display = ['title', 'author', 'created_at', 'is_active']
    list_editable = ['is_active']


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleCategory)
admin.site.register(models.ArticleTag)
admin.site.register(models.ArticleComment)
