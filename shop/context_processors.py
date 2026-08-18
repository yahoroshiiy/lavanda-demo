from .models import Product

def cart(request):
    cart_data = request.session.get("cart", {})
    ids = [int(x) for x in cart_data.keys() if str(x).isdigit()]
    products = {p.id: p for p in Product.objects.filter(id__in=ids, is_active=True)}
    items = [(products[i], int(cart_data[str(i)])) for i in ids if i in products and int(cart_data[str(i)]) > 0]
    count = sum(q for _, q in items)
    total = sum(p.price * q for p, q in items)
    cart_open = bool(request.session.pop("cart_open", False))
    return {"cart_count": count, "cart_total": total, "cart_items": items, "cart_open": cart_open}
