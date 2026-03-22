from django.db import models


# Category
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    emoji = models.CharField(max_length=10, default="🍽️") # Filter tugma emoji

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'



# Product
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    descriptions = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_hot = models.BooleanField(default=False)  # 🔥 belgisi
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

# Order
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('confirmed', 'Tasdiqlangan'),
        ('delivering', 'Yetkazilmoqda'),
        ('done', 'Bajarildi'),
        ('cancelled', 'Bekor qilindi'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Naqd pul'),
        ('card', 'Karta'),
        ('online', 'Online'),
    ]
    first_name = models.CharField(max_length=100)  # Ism
    last_name = models.CharField(max_length=100)  # Familiya
    phone = models.CharField(max_length=20)  # Telefon
    address = models.CharField(max_length=300)   # Manzil
    apartment = models.CharField(max_length=50, blank=True)  # Kvartira
    payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    promo_code = models.CharField(max_length=50, blank=True)
    total_price = models.IntegerField(default=0)  # Jami narx
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    comment = models.TextField(blank=True)    # Izoh
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Buyurtma #{self.pk} — {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-created_at']  # Yangilari birinchi


# Order Item
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)  # O'chirilgan mahsulot nomi saqlansin
    quantity = models.IntegerField(default=1)   # Miqdori
    price = models.IntegerField()  # Buyurtma vaqtidagi narx

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'

    class Meta:
        verbose_name = 'Buyurtma elementi'
        verbose_name_plural = 'Buyurtma elementlari'

# Promo code
class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)  # MAXWAY20
    discount_percent = models.IntegerField(default=0)  # 20 (%)
    is_active = models.BooleanField(default=True) # Yoqilgan/o'chirilgan
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} — {self.discount_percent}%"

    class Meta:
        verbose_name = 'Promo kod'
        verbose_name_plural = 'Promo kodlar'

