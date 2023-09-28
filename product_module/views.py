from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView

from article_module.models import Article, ArticleCategory
from utils.HTTP_service import get_client_ip
from utils.convertors import group_list
from .forms import ProductSupportForm
from .models import Product, ProductCategory, ProductBrand, ProductColorCategory, ProductVisit, ProductReview


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 12

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        brand_name = self.kwargs.get('brand')
        color_name = self.kwargs.get('color')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price', 0)
        end_price = request.GET.get('end_price', 50000000)  # Set a maximum value for end_price

        # Validate start_price and end_price as integers or set them to default values
        try:
            start_price = int(start_price)
        except ValueError:
            start_price = 0

        try:
            end_price = int(end_price)
        except ValueError:
            end_price = 50000000

        # Filter by price range
        query = query.filter(price__gte=start_price, price__lte=end_price)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if color_name is not None:
            query = query.filter(color__url_title__iexact=color_name)

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Access request and other context data here
        request = self.request

        categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        context['categories'] = categories

        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        context['article_categories'] = article_categories
        context['articles_in_article_categories'] = articles_in_article_categories

        # Add any other context data you need here

        return context


from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from .models import Product, ProductComment


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object

        request = self.request
        favorite_product_ids = request.session.get("product_favorites", [])
        context['is_favorite'] = str(loaded_product.id) in favorite_product_ids

        categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        context['categories'] = categories

        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        context['article_categories'] = article_categories
        context['articles_in_article_categories'] = articles_in_article_categories

        special_products = Product.objects.filter(is_delete=False, is_active=True,
                                                  is_in_list_special_products=True).order_by('-created_at')[:10]
        context['special_products'] = group_list(special_products)

        product = get_object_or_404(Product, slug=loaded_product.slug)
        num_reviews = ProductReview.objects.filter(product=product).count()

        context['product'] = product
        context['num_reviews'] = num_reviews

        latest_products = Product.objects.filter(is_delete=False, is_active=True).order_by('-created_at')[:10]
        context['latest_products'] = group_list(latest_products)

        user_ip = get_client_ip(self.request)
        user_id = self.request.user.id if self.request.user.is_authenticated else None

        has_been_visited = ProductVisit.objects.filter(ip=user_ip, product=loaded_product).exists()

        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product=loaded_product)
            new_visit.save()

        product_comments = ProductComment.objects.annotate(comments_count=Count('product')).filter(
            product=loaded_product, is_show=True).order_by('-create_date')
        context['product_comments'] = product_comments
        user = self.request.user

        if user.is_authenticated:
            context['user_comment'] = True

        else:
            existing_ip_comment = ProductComment.objects.filter(Q(ip=user_ip) & ~Q(user=None)).first()

            if existing_ip_comment:
                context['user_comment'] = True
                context['existing_ip_comment'] = existing_ip_comment

        return context

    def post(self, request, *args, **kwargs):
        if 'review_submit' in request.POST:
            product_slug = kwargs['slug']
            text = request.POST.get('review')
            name = request.POST.get('name')
            email = request.POST.get('email')

            # Get the product instance
            product = Product.objects.get(slug=product_slug)

            new_comment = ProductComment(
                product=product,
                name=request.POST.get('name'),
                user=request.user if request.user.is_authenticated else None,
                email=email,  # No need for email here
                text=text,
                is_show=True

            )
            new_comment.save()

            # Only create a new ProductReview if the user is authenticated123
            if request.user.is_authenticated:
                rating = int(request.POST.get('rating'))
                new_review = ProductReview(
                    product=product,
                    rating=rating,
                    user=request.user,
                )
                new_review.save()

                product.update_rating()

            return redirect('product-detail', slug=product_slug)


class MyFavoritesView(View):
    def get(self, request):
        favorite_product_ids = request.session.get("product_favorites", [])
        favorite_products = Product.objects.filter(id__in=favorite_product_ids)

        categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        context = {
            'favorite_products': favorite_products,
            'categories': categories,
            'article_categories': article_categories,
            'articles_in_article_categories': articles_in_article_categories,
            # Add any other context data you need here
        }

        return render(request, 'product_module/my_favorites.html', context)


class AddProductFavorite(View):
    def post(self, request):
        product_fav_id = request.POST.get("product_fav_id")

        # Retrieve the current list of favorite product IDs from the session
        favorite_product_ids = request.session.get("product_favorites", [])

        # Check if the product is already in the favorites list
        if product_fav_id in favorite_product_ids:
            # If the product is in the favorites list, remove it
            favorite_product_ids.remove(product_fav_id)
        else:
            # If the product is not in the favorites list, add it
            favorite_product_ids.append(product_fav_id)

        # Save the updated list of favorite product IDs back to the session
        request.session["product_favorites"] = favorite_product_ids
        # return redirect('my-favorites')  # Redirect to the list of orders page
        # return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page
        previous_page = request.META.get('HTTP_REFERER')

        if previous_page and '/products/detail/' in previous_page:
            # Redirect back to the previous product details page
            return redirect(previous_page)
        else:
            # Redirect to the product list page
            return redirect('my-favorites')  # Replace 'product-list' with your product list page name


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)


def header_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_in_header=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/header_brands_component.html', context)


def product_colors_component(request: HttpRequest):
    product_colors = ProductColorCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'colors': product_colors
    }
    return render(request, 'product_module/components/product_colors_component.html', context)


def template_preview(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    template_url = product.template_url

    context = {
        'template_url': template_url,
    }
    return render(request, 'product_module/template_preview.html', context)


class MyOrdersView(View):
    def get(self, request):
        order_product_ids = request.session.get("product_orders", [])
        order_products = Product.objects.filter(id__in=order_product_ids)
        total_price = sum(product.price for product in order_products)

        categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        context = {
            'order_products': order_products,
            'total_price': total_price,
            'categories': categories,
            'article_categories': article_categories,
            'articles_in_article_categories': articles_in_article_categories,
            # Add any other context data you need here
        }

        return render(request, 'product_module/my_orders.html', context)


from django.urls import reverse

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class AddProductOrder(View):
    def post(self, request):
        product_order_id = request.POST.get("product_order_id")

        # Retrieve the current list of order product IDs from the session
        order_product_ids = request.session.get("product_orders", [])

        # Check if the product is already in the order list
        if product_order_id in order_product_ids:
            # If the product is in the order list, remove it
            order_product_ids.remove(product_order_id)
            is_order = False  # Product is removed from the order
        else:
            # If the product is not in the order list, add it
            order_product_ids.append(product_order_id)
            is_order = True  # Product is added to the order

        # Save the updated list of order product IDs back to the session
        request.session["product_orders"] = order_product_ids

        # Determine the URL of the previous page
        previous_page = request.META.get('HTTP_REFERER')

        if previous_page and '/products/detail/' in previous_page:
            # Parse the previous URL
            parsed_url = urlparse(previous_page)

            # Get the query parameters from the parsed URL
            query_parameters = parse_qs(parsed_url.query)

            # Update the 'is_order' parameter in the query parameters
            query_parameters['is_order'] = [str(is_order)]

            # Encode the updated query parameters
            encoded_query = urlencode(query_parameters, doseq=True)

            # Construct the updated URL with the encoded query
            updated_url = urlunparse(parsed_url._replace(query=encoded_query))

            return redirect(updated_url)
        else:
            # Redirect to the product list page
            return redirect('my-orders')  # Replace 'product-list' with your product list page name


from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Proforma
from product_module.models import Product


class FinalizePaymentView(View):
    @method_decorator(login_required)
    def get(self, request):
        # Get the user's cart/order details
        order_product_ids = request.session.get("product_orders", [])
        order_products = Product.objects.filter(id__in=order_product_ids)

        # Calculate the total price
        total_price = sum(product.price for product in order_products)

        # Create a Proforma (invoice) for the user
        proforma = Proforma.objects.create(user=request.user, is_paid=False)

        # Associate the selected products with the Proforma
        proforma.products.set(order_products)

        # Redirect to the Proforma detail page
        proforma_detail_url = reverse('proforma-detail', kwargs={'proforma_id': proforma.id})
        return redirect(proforma_detail_url)


from django.views import View
from .models import Proforma


class ProformaDetailView(View):
    def get(self, request, proforma_id):
        try:
            proforma = Proforma.objects.get(pk=proforma_id)
        except Proforma.DoesNotExist:
            # Handle the case when the proforma is not found
            return render(request, 'product_module/my_orders.html')  # Replace with your error template

        context = {'proforma': proforma}
        return render(request, 'product_module/my-proforma.html',
                      context)  # Replace with your proforma detail template


from django.shortcuts import render
from .models import ProductCategory


# class ProductSupportView(View):
#     def get(self, request):
#         productsupport_form = ProductSupportForm()
#         return render(request, 'product_module/product_support.html', {
#             'productsupport_form': productsupport_form
#         })
#
#     def post(self, request):
#         productsupport_form = ProductSupportForm(request.POST)
#         user = self.request.user
#         if productsupport_form.is_valid():
#             productsupport_form.save()
#             return redirect('home_page')
#
#         return render(request, 'product_module/product_support.html', {
#             'productsupport_form': productsupport_form
#         })

class ProductSupportView(View):
    def get(self, request):
        productsupport_form = ProductSupportForm()

        # Retrieve the categories and articles here
        product_categories = ProductCategory.objects.filter(is_delete=False, is_active=True, is_in_listCat_homepage=True)
        article_categories = ArticleCategory.objects.filter(is_delete=False, is_active=True)
        articles_in_article_categories = []

        for category in article_categories:
            articles = Article.objects.filter(is_delete=False, is_active=True, category=category)[:8]
            articles_in_article_categories.append((category, articles))

        return render(request, 'product_module/product_support.html', {
            'productsupport_form': productsupport_form,
            'product_categories': product_categories,
            'article_categories': article_categories,
            'articles_in_article_categories': articles_in_article_categories
        })
