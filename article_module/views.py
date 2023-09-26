from django.shortcuts import render
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView
from product_module.models import ProductCategory
from utils.HTTP_service import get_client_ip
from utils.convertors import group_list
from .models import Article, ArticleComment, ArticleCategory


class ArticleListView(ListView):
    template_name = 'article_module/article_list.html'
    model = Article
    context_object_name = 'articles'
    ordering = ['-created_at']
    paginate_by = 12

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        request: HttpRequest = self.request

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch categories and articles as needed
        categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        context['categories'] = categories
        context['article_categories'] = article_categories
        context['articles_in_article_categories'] = articles_in_article_categories

        return context


class ArticleDetailView(DetailView):
    template_name = 'article_module/article_detail.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_article = self.object

        # Retrieve comments associated with the article that are marked as is_show=True
        article_comments = ArticleComment.objects.filter(product=loaded_article, is_show=True)

        context['article_comments'] = article_comments

        latest_articles = Article.objects.filter(is_delete=False, is_active=True).order_by('-created_at')[:10]
        context['latest_articles'] = group_list(latest_articles)

        # Check if the user is authenticated (logged in)
        user = self.request.user

        # If the user is authenticated, their comment will be linked to their user account
        if user.is_authenticated:
            context['user_comment'] = True

        # If the user is not authenticated, check if an IP-based comment already exists
        else:
            user_ip = get_client_ip(self.request)
            existing_ip_comment = ArticleComment.objects.filter(Q(ip=user_ip) & ~Q(user=None)).first()

            if existing_ip_comment:
                context['user_comment'] = True
                context['existing_ip_comment'] = existing_ip_comment

        # Fetch categories and articles as needed
        categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        context['categories'] = categories
        context['article_categories'] = article_categories
        context['articles_in_article_categories'] = articles_in_article_categories

        return context

    def post(self, request, *args, **kwargs):
        if 'comment_submit' in request.POST:
            article_slug = kwargs['slug']
            text = request.POST.get('comment')
            author = request.POST.get('author')
            email = request.POST.get('email_1')

            # Get the article instance
            article = Article.objects.get(slug=article_slug)

            # Create a new ArticleComment instance
            new_comment = ArticleComment(
                product=article,
                ip=get_client_ip(request),
                user=request.user if request.user.is_authenticated else None,
                email=email,
                text=text,
                is_show=False  # Set to False, comment needs approval
            )

            new_comment.save()

            # Redirect back to the article detail page
            return redirect('article-detail', slug=article_slug)
