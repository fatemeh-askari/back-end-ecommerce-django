# from django.shortcuts import render
# from django.db.models import Q
# from .forms import ProductSearchForm
# from product_module.models import Product, ProductTag, ProductReview, ProductCategory
# from article_module.models import Article, ArticleTag  # Import Article and ArticleTag models
#
#
# def product_search(request):
#     query = request.GET.get('query')
#     form = ProductSearchForm(initial={'query': query})  # Set the initial value
#
#     products = Product.objects.none()
#     articles = Article.objects.none()
#
#     if query:
#         # Search for products
#         products = Product.objects.filter(
#             Q(title__icontains=query) |  # Search by product title
#             Q(description__icontains=query) |  # Search by product description
#             Q(product_tags__caption__icontains=query)  # Search by product tags
#         ).distinct()
#
#         # Search for articles
#         articles = Article.objects.filter(
#             Q(title__icontains=query) |  # Search by article title
#             Q(description__icontains=query) |  # Search by article description
#             Q(article_tags__caption__icontains=query)  # Search by article tags (adjust the related name accordingly)
#         ).distinct()
#
#         # You can add additional filters here based on form fields
#
#     context = {
#         'form': form,
#         'products': products,
#         'articles': articles,  # Include the articles in the context
#     }
#     return render(request, 'search_module/search_result.html', context)

from django.shortcuts import render
from django.db.models import Q
from .forms import ProductSearchForm
from product_module.models import Product, ProductTag, ProductReview, ProductCategory
from article_module.models import Article, ArticleTag, ArticleCategory  # Import Article, ArticleTag, and ArticleCategory models

def product_search(request):
    query = request.GET.get('query')
    form = ProductSearchForm(initial={'query': query})

    products = Product.objects.none()
    articles = Article.objects.none()

    if query:
        # Search for products
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(product_tags__caption__icontains=query)
        ).distinct()

        # Search for articles
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(article_tags__caption__icontains=query)
        ).distinct()

    # Fetch product categories and articles in article categories
    product_categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
    article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
    articles_in_article_categories = []

    for category in article_categories:
        articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
        articles_in_article_categories.append((category, articles))

    context = {
        'form': form,
        'products': products,
        'articles': articles,
        'product_categories': product_categories,  # Include product categories
        'articles_in_article_categories': articles_in_article_categories,  # Include articles in article categories
    }
    return render(request, 'search_module/search_result.html', context)



