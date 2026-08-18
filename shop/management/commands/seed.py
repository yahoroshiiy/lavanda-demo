from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = "Создаёт демо-категории и букеты"

    def handle(self, *args, **kwargs):
        cats = {
            "roses": "Розы",
            "mixed": "Сборные",
            "minimal": "Минимализм",
        }
        for slug, name in cats.items():
            Category.objects.get_or_create(slug=slug, defaults={"name": name})

        data = [
            ("Розовый рассвет", "roses", 3490, True, "Нежный букет из розовых роз", "https://images.unsplash.com/photo-1523438885200-e635ba2c371e?auto=format&fit=crop&w=900&q=85"),
            ("Нежность", "mixed", 2990, True, "Воздушная композиция в пастельных оттенках", "https://images.unsplash.com/photo-1509223197845-458d87318791?auto=format&fit=crop&w=900&q=85"),
            ("Белая классика", "minimal", 2790, False, "Лаконичный букет в светлой гамме", "https://images.unsplash.com/photo-1561181286-d3fee7d55364?auto=format&fit=crop&w=900&q=85"),
            ("Весеннее настроение", "mixed", 3290, False, "Яркая сезонная композиция", "https://images.unsplash.com/photo-1525310072745-f49212b5ac6d?auto=format&fit=crop&w=900&q=85"),
            ("Пудровая любовь", "roses", 4190, True, "Пышный букет для особенного повода", "https://images.unsplash.com/photo-1495231916356-a86217efff12?auto=format&fit=crop&w=900&q=85"),
            ("Лёгкий день", "minimal", 2490, False, "Небольшой букет для знака внимания", "https://images.unsplash.com/photo-1497250681960-ef046c08a56e?auto=format&fit=crop&w=900&q=85"),
            ("Тёплое чувство", "mixed", 3790, False, "Композиция в тёплых оттенках", "https://images.unsplash.com/photo-1487070183336-b863922373d4?auto=format&fit=crop&w=900&q=85"),
            ("Для тебя", "roses", 4490, True, "Премиальная композиция из свежих роз", "https://images.unsplash.com/photo-1518709594023-6eab9bab7b23?auto=format&fit=crop&w=900&q=85"),
        ]
        for name, slug, price, hit, desc, image in data:
            Product.objects.update_or_create(
                name=name,
                defaults={
                    "category": Category.objects.get(slug=slug),
                    "price": price,
                    "is_hit": hit,
                    "description": desc,
                    "image": image,
                    "is_active": True,
                },
            )
        self.stdout.write(self.style.SUCCESS("Демо-данные созданы."))
