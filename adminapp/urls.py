from django.urls import path
from .views import *

urlpatterns = [
    path('', shop_home, name='shop_home'),
    path('order/', shop_order, name='shop_order'),
    path('order/success/', order_success, name='order_success'),
    path('check-promo/', check_promo, name='check_promo'),
]