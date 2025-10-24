from django.contrib import admin
from .models import Product, ProductImage, Category, Order, OrderItem, Profile

# --- Інлайн для додаткових фото ---
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('id',)

# --- Адмін для продукту ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'order')
    list_editable = ('order',)
    list_filter = ('category',)
    search_fields = ('name', 'description')
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'price', 'category', 'image', 'description')
        }),
        ('Деталі', {
            'fields': ('ingredients', 'usage_instructions', 'order')
        }),
    )
    inlines = [ProductImageInline]

# --- Адмін для категорії ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# --- Інлайн для товарів замовлення ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price')

# --- Адмін для замовлення ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

# --- Адмін для профілю користувача ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'address', 'promo_code')