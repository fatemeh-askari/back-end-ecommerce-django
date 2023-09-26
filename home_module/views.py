from django.db.models import Count, Q
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from article_module.models import ArticleCategory, Article
from product_module.models import Product, ProductCategory
from site_module.models import SiteSetting, FooterLinkBox
from utils.convertors import group_list
from django.shortcuts import get_object_or_404


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_special_products1(self):
        # Retrieve products with is_special_products1=True that are active and not deleted
        return Product.objects.filter(is_special_products1=True, is_active=True, is_delete=False)

    def get_homepage1_category_title(self):
        # Retrieve the category that has 'is_in_homepage1' set to True
        try:
            homepage1_category = ProductCategory.objects.get(is_delete=False, is_active=True, is_in_homepage1=True)
            return homepage1_category.title
        except ProductCategory.DoesNotExist:
            return None

    def get_homepage2_category_title(self):
        # Retrieve the category that has 'is_in_homepage2' set to True
        try:
            homepage2_category = ProductCategory.objects.get(is_delete=False, is_active=True, is_in_homepage2=True)
            return homepage2_category.title
        except ProductCategory.DoesNotExist:
            return None

    def get_homepage3_category_title(self):
        # Retrieve the category that has 'is_in_homepage3' set to True
        try:
            homepage3_category = ProductCategory.objects.get(is_delete=False, is_active=True, is_in_homepage3=True)
            return homepage3_category.title
        except ProductCategory.DoesNotExist:
            return None

    def get_homepage1_category_image(self):
        # Retrieve the image URL for the category that has 'is_in_homepage1' set to True
        try:
            homepage1_category = ProductCategory.objects.get(is_delete=False, is_active=True, is_in_homepage1=True)
            return homepage1_category.image.url if homepage1_category.image else None
        except ProductCategory.DoesNotExist:
            return None

    def get_homepage2_category_image(self):
        # Retrieve the image URL for the category that has 'is_in_homepage2' set to True
        try:
            homepage2_category = ProductCategory.objects.get(is_delete=False, is_active=True, is_in_homepage2=True)
            return homepage2_category.image.url if homepage2_category.image else None
        except ProductCategory.DoesNotExist:
            return None

    def get_homepage3_category_image(self):
        # Retrieve the image URL for the category that has 'is_in_homepage3' set to True
        try:
            homepage3_category = ProductCategory.objects.get(is_delete=False, is_active=True, is_in_homepage3=True)
            return homepage3_category.image.url if homepage3_category.image else None
        except ProductCategory.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'this is data in home page'
        context['message'] = 'this is message in home page'

        most_visit_products = Product.objects.filter(is_delete=False, is_active=True).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:10]
        context['most_visit_products'] = group_list(most_visit_products)

        latest_products = Product.objects.filter(is_delete=False, is_active=True).order_by('-created_at')[:10]
        context['latest_products'] = group_list(latest_products)

        special_products = Product.objects.filter(is_delete=False, is_active=True,
                                                  is_in_list_special_products=True).order_by('-created_at')[:10]
        context['special_products'] = group_list(special_products)

        categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        context['categories'] = categories

        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        context['article_categories'] = article_categories
        context['articles_in_article_categories'] = articles_in_article_categories

        latest_articles = Article.objects.filter(is_delete=False, is_active=True).order_by('created_at')[:4]
        context['latest_articles'] = group_list(latest_articles)

        # Retrieve categories that have 'is_in_homepage1' set to True
        homepage1_categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_homepage1=True)
        homepage1_category_url_titles = [category.url_title for category in homepage1_categories]

        # Create a list to store products for each category in 'homepage1_categories'
        homepage1_products = []
        for category in homepage1_categories:
            products = Product.objects.filter(is_delete=False, is_active=True, category=category)
            # Slice the products list to only keep the last 8 elements
            homepage1_products.append(products[:8])

        # Retrieve categories that have 'is_in_homepage2' set to True
        homepage2_categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_homepage2=True)
        homepage2_category_url_titles = [category.url_title for category in homepage2_categories]

        # Create a list to store products for each category in 'homepage2_categories'
        homepage2_products = []
        for category in homepage2_categories:
            products = Product.objects.filter(is_delete=False, is_active=True, category=category)
            # Slice the products list to only keep the last 8 elements
            homepage2_products.append(products[:8])

        # Retrieve categories that have 'is_in_homepage3' set to True
        homepage3_categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_homepage3=True)
        homepage3_category_url_titles = [category.url_title for category in homepage3_categories]

        # Create a list to store products for each category in 'homepage3_categories'
        homepage3_products = []
        for category in homepage3_categories:
            products = Product.objects.filter(is_delete=False, is_active=True, category=category)
            # Slice the products list to only keep the last 8 elements
            homepage3_products.append(products[:8])

        # Add 'homepage1_products', 'homepage2_products', and 'homepage3_products' to the context
        context['homepage1_products'] = homepage1_products
        context['homepage2_products'] = homepage2_products
        context['homepage3_products'] = homepage3_products

        # Call the new functions to get the category titles for each section and add them to the context
        context['homepage1_category_title'] = self.get_homepage1_category_title()
        context['homepage2_category_title'] = self.get_homepage2_category_title()
        context['homepage3_category_title'] = self.get_homepage3_category_title()

        context['homepage1_category_image'] = self.get_homepage1_category_image()
        context['homepage2_category_image'] = self.get_homepage2_category_image()
        context['homepage3_category_image'] = self.get_homepage3_category_image()

        context['homepage1_category_url_titles'] = homepage1_category_url_titles
        context['homepage2_category_url_titles'] = homepage2_category_url_titles
        context['homepage3_category_url_titles'] = homepage3_category_url_titles

        special_products1 = self.get_special_products1()
        context['special_products1'] = special_products1

        return context


class HomeCategoryListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the category URL title from the URL
        category_url_title = self.kwargs.get('category')

        # Filter by category URL title
        if category_url_title:
            category = get_object_or_404(ProductCategory, url_title=category_url_title)
            queryset = queryset.filter(category=category)

        return queryset


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    for item in footer_link_boxes:
        item.footerlink_set
    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context
