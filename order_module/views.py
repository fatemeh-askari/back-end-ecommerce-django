from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Product, Order, OrderDetail
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.utils import timezone

from django.shortcuts import render


def add_product_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity", 1)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            response_data = {"status": "error", "message": "Product not found"}
            return JsonResponse(response_data, status=404)

        if request.user.is_authenticated:
            user = request.user
            order, created = Order.objects.get_or_create(user=user, is_paid=False)
            session_key = None
        else:
            # If the user is not logged in, use the session key
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            order, created = Order.objects.get_or_create(session_key=session_key, is_paid=False)

        # Use transaction.on_commit to ensure signals are triggered after the transaction is committed
        with transaction.atomic():
            # Create a new order detail entry for the product
            order_detail = OrderDetail(order=order, product=product, final_price=product.price)
            order_detail.save()

        # Render a template with a success message
        context = {"message": "Product added to cart successfully"}
        return render(request, "order_module/order-list.html", context)

    # If the request method is not POST, return an error response
    response_data = {"status": "error", "message": "Invalid request method"}
    return JsonResponse(response_data, status=400)


from django.shortcuts import redirect


def remove_product_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        # Assuming the user is logged in, you can get the user's cart
        user = request.user
        order = Order.objects.get(user=user, is_paid=False)

        # Remove the product from the cart
        order.orderdetail_set.filter(product_id=product_id).delete()

        # Redirect back to the cart page
        return redirect("remove-order")  # Replace "cart" with the actual URL name for the cart page

    return redirect("product-list")  # Redirect to the home page for any other request method


def order_list(request):
    return render(request, 'order_module/order-list.html')


def remove_from_order_list(request):
    return render(request, 'order_module/remove_from_order-list.html')
