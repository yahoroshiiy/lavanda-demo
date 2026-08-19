import json
from .models import Product

def cart(request):
    products = Product.objects.filter(is_active=True)
    data = [
        {"id": p.id, "name": p.name, "price": float(p.price), "image": p.image, "description": p.description or "Авторский букет • свежие цветы", "category_name": p.category.name if p.category else "Цветы"}
        for p in products
    ]
    # Cart is deliberately client-side for the Vercel demo: no database/session writes.
    return {"products_json": json.dumps(data, ensure_ascii=False)}
