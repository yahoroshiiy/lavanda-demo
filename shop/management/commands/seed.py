from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = "Создаёт демо-категории и реалистичный каталог LAVANDA"

    def handle(self, *args, **kwargs):
        cats = {
            "roses": "Розы",
            "mixed": "Сборные",
            "minimal": "Лаконичные",
        }
        for slug, name in cats.items():
            Category.objects.get_or_create(slug=slug, defaults={"name": name})

        data = [
            ("Розовый сад", "roses", 4290, True, "Пышный букет из розовых роз, эвкалипта и сезонной зелени.", "https://images.unsplash.com/photo-1526045612212-70caf35c14df?auto=format&fit=crop&w=1000&q=88"),
            ("Пионовая дымка", "mixed", 4890, True, "Нежная пастельная композиция с пионами, садовыми розами и ранункулюсами.", "https://images.unsplash.com/photo-1523438885200-e635ba2c371e?auto=format&fit=crop&w=1000&q=88"),
            ("Белая классика", "minimal", 3790, False, "Белые садовые розы, эвкалипт и немного воздушной зелени.", "https://images.unsplash.com/photo-1561181286-d3fee7d55364?auto=format&fit=crop&w=1000&q=88"),
            ("Сезонный букет", "mixed", 3590, False, "Живой сборный букет в оттенках кремового, персикового и зелёного.", "https://images.unsplash.com/photo-1525310072745-f49212b5ac6d?auto=format&fit=crop&w=1000&q=88"),
            ("Пудровая любовь", "roses", 5290, True, "Премиальная композиция из пудровых роз с мягкой зеленью.", "https://images.unsplash.com/photo-1495231916356-a86217efff12?auto=format&fit=crop&w=1000&q=88"),
            ("Лёгкий день", "minimal", 2990, False, "Небольшой букет в спокойной гамме — для знака внимания без повода.", "https://images.unsplash.com/photo-1468327768560-75b778cbb551?auto=format&fit=crop&w=1000&q=88"),
            ("Красный акцент", "roses", 4590, False, "Выразительные красные розы, собранные в классическую круглую форму.", "https://images.unsplash.com/photo-1518709594023-6eab9bab7b23?auto=format&fit=crop&w=1000&q=88"),
            ("Тихая роскошь", "minimal", 5590, True, "Сдержанная композиция в молочно-зелёной гамме для особенного события.", "https://images.unsplash.com/photo-1457089328109-e5d9bd499191?auto=format&fit=crop&w=1000&q=88"),
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
        self.stdout.write(self.style.SUCCESS("Каталог LAVANDA обновлён."))
