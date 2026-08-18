# Generated manually for the demo project.
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("slug", models.SlugField(max_length=50, unique=True, verbose_name="Slug")),
            ],
            options={"verbose_name": "Категория", "verbose_name_plural": "Категории"},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180, verbose_name="Название")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Цена")),
                ("image", models.URLField(verbose_name="URL изображения")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать")),
                ("is_hit", models.BooleanField(default=False, verbose_name="Хит")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="shop.category", verbose_name="Категория")),
            ],
            options={"verbose_name": "Букет", "verbose_name_plural": "Букеты", "ordering": ["-is_hit", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Имя")),
                ("phone", models.CharField(max_length=40, verbose_name="Телефон")),
                ("address", models.CharField(max_length=255, verbose_name="Адрес")),
                ("delivery_time", models.CharField(blank=True, max_length=100, verbose_name="Время доставки")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий")),
                ("total", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Сумма")),
                ("status", models.CharField(choices=[("new", "Новый"), ("confirmed", "Подтверждён"), ("delivery", "Передан в доставку"), ("done", "Выполнен"), ("cancelled", "Отменён")], default="new", max_length=20, verbose_name="Статус")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
            ],
            options={"verbose_name": "Заказ", "verbose_name_plural": "Заказы", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Цена")),
                ("quantity", models.PositiveIntegerField(default=1, verbose_name="Количество")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="shop.order", verbose_name="Заказ")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="shop.product", verbose_name="Букет")),
            ],
            options={"verbose_name": "Позиция заказа", "verbose_name_plural": "Позиции заказа"},
        ),
    ]
