from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Product, Order, OrderItem

def home(request):
    products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    return render(request, "shop/home.html", {"products": products, "categories": categories})

def catalog(request):
    products = Product.objects.filter(is_active=True)
    category = request.GET.get("category")
    if category:
        products = products.filter(category__slug=category)
    return render(request, "shop/catalog.html", {
        "products": products,
        "categories": Category.objects.all(),
        "selected": category,
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = request.session.get("cart", {})
    key = str(product.id)
    cart[key] = int(cart.get(key, 0)) + 1
    request.session["cart"] = cart
    request.session["cart_open"] = True
    messages.success(request, f"«{product.name}» добавлен в корзину")
    return redirect(request.META.get("HTTP_REFERER", "home"))

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    key = str(product_id)
    if key in cart:
        if int(cart[key]) > 1:
            cart[key] = int(cart[key]) - 1
        else:
            del cart[key]
    request.session["cart"] = cart
    return redirect("cart")

def cart(request):
    cart_data = request.session.get("cart", {})
    products = Product.objects.filter(id__in=[int(x) for x in cart_data.keys()], is_active=True)
    items = [(p, int(cart_data.get(str(p.id), 0))) for p in products]
    total = sum(p.price * q for p, q in items)
    return render(request, "shop/cart.html", {"items": items, "total": total})

@transaction.atomic
def checkout(request):
    cart_data = request.session.get("cart", {})
    products = Product.objects.filter(id__in=[int(x) for x in cart_data.keys()], is_active=True)
    items = [(p, int(cart_data.get(str(p.id), 0))) for p in products]
    if not items:
        return redirect("catalog")
    total = sum(p.price * q for p, q in items)
    if request.method == "POST":
        order = Order.objects.create(
            name=request.POST.get("name", ""),
            phone=request.POST.get("phone", ""),
            address=request.POST.get("address", ""),
            delivery_time=request.POST.get("delivery_time", ""),
            comment=request.POST.get("comment", ""),
            total=total,
        )
        for product, quantity in items:
            OrderItem.objects.create(order=order, product=product, price=product.price, quantity=quantity)
        request.session["cart"] = {}
        return redirect("order_success", order_id=order.id)
    return render(request, "shop/checkout.html", {"items": items, "total": total})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/success.html", {"order": order})
