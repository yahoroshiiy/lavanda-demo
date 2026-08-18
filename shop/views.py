from django.shortcuts import render
from .models import Category, Product

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

def cart(request):
    return render(request, "shop/cart.html")

def checkout(request):
    return render(request, "shop/checkout.html")

def order_success(request):
    return render(request, "shop/success.html")
