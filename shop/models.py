from django.db import models

class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("Название", max_length=180)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.URLField("URL изображения")
    is_active = models.BooleanField("Показывать", default=True)
    is_hit = models.BooleanField("Хит", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"
        ordering = ["-is_hit", "-created_at"]

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = [
        ("new", "Новый"),
        ("confirmed", "Подтверждён"),
        ("delivery", "Передан в доставку"),
        ("done", "Выполнен"),
        ("cancelled", "Отменён"),
    ]
    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=40)
    address = models.CharField("Адрес", max_length=255)
    delivery_time = models.CharField("Время доставки", max_length=100, blank=True)
    comment = models.TextField("Комментарий", blank=True)
    total = models.DecimalField("Сумма", max_digits=10, decimal_places=2, default=0)
    status = models.CharField("Статус", max_length=20, choices=STATUS, default="new")
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk} — {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Букет")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
