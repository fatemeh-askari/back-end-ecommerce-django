from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from article_module.models import ArticleCategory, Article
from product_module.models import ProductCategory
from site_module.models import SiteSetting
from .forms import ContactUsForm
from django.views.generic.edit import CreateView

from .models import UserProfile


class ContactUsView(View):
    def get(self, request):
        contact_form = ContactUsForm()
        categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        return render(request, 'contact_module/contact_us_page.html', {
            'contact_form': contact_form,
            'categories': categories,
            'article_categories': article_categories,
            'articles_in_article_categories': articles_in_article_categories,
            # Add other context data here
        })

    def post(self, request):
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('home_page')

        categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        return render(request, 'contact_module/contact_us_page.html', {
            'contact_form': contact_form,
            'categories': categories,
            'article_categories': article_categories,
            'articles_in_article_categories': articles_in_article_categories,
            # Add other context data here
        })

class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile'


class ProfilesView(ListView):
    model = UserProfile
    template_name = 'contact_module/profiles_list_page.html'
    context_object_name = 'profiles'
