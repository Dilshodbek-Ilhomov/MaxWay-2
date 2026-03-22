import json
from django.shortcuts import render, redirect
from adminapp.models import Category, Product, Order, OrderItem, PromoCode
from django.http import JsonResponse

def shop_home(request):
    """Asosiy sahifa — barcha mahsulotlar kategoriyalar bo'yicha"""
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).select_related('category')
    ctx = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/index.html', ctx)


def shop_order(request):
    if request.method == 'POST':
        # Formadan ma'lumotlarni olish
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        apartment = request.POST.get('apartment', '')
        payment = request.POST.get('payment', 'cash')
        promo = request.POST.get('promo', '').strip().upper()
        comment = request.POST.get('comment', '')
        cart_json = request.POST.get('cart', '[]')

        try:
            cart = json.loads(cart_json)
        except:
            cart = []

        # Promo kodni tekshirish
        discount_percent = 0
        try:
            promo_obj = PromoCode.objects.get(code=promo, is_active=True)
            discount_percent = promo_obj.discount_percent
        except PromoCode.DoesNotExist:
            pass

        # Buyurtmani yaratish
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            apartment=apartment,
            payment=payment,
            promo_code=promo,
            comment=comment,
        )

        # Buyurtma elementlarini yaratish
        total = 0
        for item in cart:
            product_id = item.get('id')
            qty = int(item.get('qty', 1))
            try:
                product = Product.objects.get(pk=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=qty,
                    price=product.price,
                )
                total += product.price * qty
            except Product.DoesNotExist:
                pass

        # Chegirmani qo'llash
        if discount_percent > 0:
            total = total - (total * discount_percent // 100)

        order.total_price = total
        order.save()

        # Order ID ni session orqali uzatamiz
        request.session['last_order_id'] = order.pk

        return redirect('order_success')

    return render(request, 'shop/order.html')


def check_promo(request):
    """Promo kodni AJAX orqali tekshirish"""
    code = request.GET.get('code', '').strip().upper()
    try:
        promo = PromoCode.objects.get(code=code, is_active=True)
        return JsonResponse({'valid': True, 'discount': promo.discount_percent})
    except PromoCode.DoesNotExist:
        return JsonResponse({'valid': False})

def order_success(request):
    """Buyurtma muvaffaqiyatli qabul qilindi sahifasi"""
    order_id = request.session.pop('last_order_id', None)
    return render(request, 'shop/success.html', {'order_id': order_id})