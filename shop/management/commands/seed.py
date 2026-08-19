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
            ("Розовый сад", "roses", 4290, True, "Пышная композиция из розовых роз и нежной зелени.", "https://images.pexels.com/photos/16131098/pexels-photo-16131098.jpeg?auto=compress&cs=tinysrgb&w=1000"),
            ("Белая классика", "minimal", 3790, True, "Воздушный букет из белых роз в спокойной элегантной гамме.", "https://images.pexels.com/photos/18310105/pexels-photo-18310105.jpeg?auto=compress&cs=tinysrgb&w=1000"),
            ("Пионовое облако", "mixed", 5190, True, "Нежные розовые пионы и сезонная зелень — мягкий акцент для особенного дня.", "https://images.pexels.com/photos/26241142/pexels-photo-26241142.jpeg?auto=compress&cs=tinysrgb&w=1000"),
            ("Нежный рассвет", "mixed", 4590, False, "Сочетание розовых и белых роз в лёгкой натуральной упаковке.", "https://images.pexels.com/photos/13475845/pexels-photo-13475845.jpeg?auto=compress&cs=tinysrgb&w=1000"),
            ("Розовый шелк", "roses", 4890, True, "Плотный букет из ярких роз — выразительный и праздничный.", "https://images.pexels.com/photos/1447367/pexels-photo-1447367.jpeg?auto=compress&cs=tinysrgb&w=1000"),
            ("Весенние тюльпаны", "mixed", 3290, False, "Свежие розовые тюльпаны с зеленью — лёгкий букет без лишней торжественности.", "https://images.pexels.com/photos/11423480/pexels-photo-11423480.jpeg?auto=compress&cs=tinysrgb&w=1000"),
            ("Красный акцент", "roses", 5290, False, "Классические красные розы для сильного и красивого жеста.", "https://images.pexels.com/photos/17352951/pexels-photo-17352951.jpeg?auto=compress&cs=tinysrgb&w=1000"),
            ("Садовая история", "minimal", 5590, True, "Смешанная композиция из садовых роз и зелени с естественной фактурой.", "https://images.pexels.com/photos/19174029/pexels-photo-19174029.jpeg?auto=compress&cs=tinysrgb&w=1000"),
        ]
        Product.objects.exclude(name__in=[row[0] for row in data]).update(is_active=False)
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
