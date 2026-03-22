from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem, PromoCode


# Mahsulot admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'emoji']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'category', 'price', 'is_available', 'is_hot']
    list_filter = ['category', 'is_available', 'is_hot']
    list_editable = ['price', 'is_available', 'is_hot']
    search_fields = ['name']

    @admin.display(description='Rasm')
    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:52px;height:52px;object-fit:cover;'
                'border-radius:10px;border:1px solid rgba(255,255,255,0.12);" />',
                obj.image.url
            )
        return format_html(
            '<div style="width:52px;height:52px;border-radius:10px;'
            'background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.10);'
            'display:flex;align-items:center;justify-content:center;font-size:20px;">🍽️</div>'
        )


class OrderItemInline(admin.TabularInline):  # Buyurtma ichida elementlar
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'payment', 'created_at']
    list_editable = ['status']  # Statusni ro'yxatda o'zgartirish
    readonly_fields = ['first_name', 'last_name', 'phone', 'address', 'total_price', 'created_at']
    inlines = [OrderItemInline]  # Buyurtma ichida mahsulotlarni ko'rish
    search_fields = ['first_name', 'last_name', 'phone']

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'is_active', 'created_at']
    list_editable = ['is_active']




# ── Custom AdminSite — dashboard'da haqiqiy sonlar ──
class MaxwayAdminSite(admin.AdminSite):
    site_header = 'Maxway Admin'
    site_title  = 'Maxway Admin'
    index_title = 'Boshqaruv Paneli'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['order_count']    = Order.objects.count()
        extra_context['product_count']  = Product.objects.count()
        extra_context['category_count'] = Category.objects.count()
        extra_context['promo_count']    = PromoCode.objects.filter(is_active=True).count()
        return super().index(request, extra_context=extra_context)


# Patch default Django admin index to inject real counts
_orig_index = admin.site.__class__.index
def _patched_index(self, request, extra_context=None):
    extra_context = extra_context or {}
    try:
        extra_context['order_count']    = Order.objects.count()
        extra_context['product_count']  = Product.objects.count()
        extra_context['category_count'] = Category.objects.count()
        extra_context['promo_count']    = PromoCode.objects.filter(is_active=True).count()
        extra_context['sys_default']    = [
            "Django Admin", "Ma'lumotlar bazasi",
            "Media fayllar", "Static fayllar",
            "I18n (uz/en)", "Promo tizim",
        ]
    except Exception:
        pass
    return _orig_index(self, request, extra_context=extra_context)

admin.site.__class__.index = _patched_index
