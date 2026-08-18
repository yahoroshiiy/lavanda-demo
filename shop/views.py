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
    messages.success(request, f"«{product.name}» добавлен в корзину")
    referer = request.META.get("HTTP_REFERER")
    if referer:
        from urllib.parse import urlsplit, parse_qsl, urlencode, urlunsplit
        parts = urlsplit(referer)
        query = dict(parse_qsl(parts.query))
        query["cart"] = "1"
        referer = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
        return redirect(referer)
    return redirect("home")

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

def checkout(request):
    cart_data = request.session.get("cart", {})
    ids = [int(x) for x in cart_data.keys() if str(x).isdigit()]
    products = Product.objects.filter(id__in=ids, is_active=True)
    items = [(p, int(cart_data.get(str(p.id), 0))) for p in products if int(cart_data.get(str(p.id), 0)) > 0]
    if not items:
        return redirect("catalog")
    total = sum(p.price * q for p, q in items)

    if request.method == "POST":
        # Demo checkout: deliberately stops before payment/database write.
        # This keeps the Vercel demo fully functional on a read-only filesystem.
        request.session["demo_order"] = {
            "name": request.POST.get("name", ""),
            "phone": request.POST.get("phone", ""),
            "address": request.POST.get("address", ""),
            "delivery_time": request.POST.get("delivery_time", ""),
            "comment": request.POST.get("comment", ""),
            "total": str(total),
            "items": [{"name": p.name, "quantity": q, "price": str(p.price)} for p, q in items],
        }
        request.session["cart"] = {}
        return redirect("order_success")

    return render(request, "shop/checkout.html", {"items": items, "total": total})

def order_success(request):
    order = request.session.get("demo_order")
    if not order:
        return redirect("home")
    return render(request, "shop/success.html", {"order": order})
