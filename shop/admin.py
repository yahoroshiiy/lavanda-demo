from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active", "is_hit", "created_at")
    list_filter = ("category", "is_active", "is_hit")
    search_fields = ("name", "description")
    list_editable = ("price", "is_active", "is_hit")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price", "quantity")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "total", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "phone", "address")
    list_editable = ("status",)
    readonly_fields = ("total", "created_at")
    inlines = [OrderItemInline]

admin.site.site_header = "LAVANDA FLOWERS"
admin.site.site_title = "LAVANDA — управление"
admin.site.index_title = "Управление магазином"
