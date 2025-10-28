from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Category


# ---------------------- Каталог ----------------------
def katalog(request, category_slug=None):
    query = request.GET.get('q', '').lower()
    categories = Category.objects.all()
    products = Product.objects.all()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Фильтр за категорією
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None

    # Фільтр за пошуком
    if query:
        products = products.filter(name__icontains=query)

    # Фільтр по ціні
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Сортировка после всех фильтров по полю order, затем id
    products = products.order_by('order', 'id').distinct()

    # Рекомендовано: наприклад, випадкові 6 товарів
    recommended_products = Product.objects.order_by('?')[:6]

    context = {
        "products": products,
        "search_query": query,
        "categories": categories,
        "current_category": category,
        "min_price": min_price or '',
        "max_price": max_price or '',
        "recommended_products": recommended_products
    }

    return render(request, 'shop/katalog.html', context)


# ---------------------- Деталі товару ----------------------
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})


# ---------------------- Додати до кошика ----------------------
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', [])

    # Перевірка: чи вже є товар у кошику
    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += 1
            item['total_price'] = float(item['price']) * item['quantity']
            break
    else:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url,
            'quantity': 1,
            'total_price': float(product.price)
        })

    request.session['cart'] = cart
    return redirect('cart')


# ---------------------- Кошик ----------------------
def cart(request):
    cart_items = request.session.get('cart', [])
    total_price = sum(float(item['total_price']) for item in cart_items)
    return render(request, 'shop/cart.html', {
        "cart_items": cart_items,
        "total_price": total_price
    })


# ---------------------- Видалити товар ----------------------
def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
        request.session['cart'] = cart
    return redirect('cart')


# ---------------------- Очистити кошик ----------------------
def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart')


# ---------------------- Оновити кількість ----------------------
def update_cart(request):
    if request.method == "POST":
        index = int(request.POST.get("index", -1))
        quantity = int(request.POST.get("quantity", 1))
        cart = request.session.get('cart', [])
        if 0 <= index < len(cart):
            cart[index]['quantity'] = quantity
            cart[index]['total_price'] = float(cart[index]['price']) * quantity
        request.session['cart'] = cart
    return redirect('cart')


# ---------------------- Оформлення замовлення ----------------------
def checkout(request):
    cart_items = request.session.get('cart', [])
    if not cart_items:
        return redirect('katalog')

    total_price = sum(float(item['total_price']) for item in cart_items)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Імітація оплати
        import time
        time.sleep(5)

        # Використовуємо користувача з id=1
        from django.contrib.auth.models import User
        user = User.objects.get(id=1)

        # Створюємо замовлення лише з user
        order = Order.objects.create(user=user)

        # Додавання товарів у замовлення
        for item in cart_items:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity']
            )

        # Очистити кошик
        request.session['cart'] = []

        # Передаємо дані просто для відображення
        return render(request, 'shop/checkout_success.html', {
            "name": name,
            "total_price": total_price
        })

    return render(request, 'shop/checkout.html', {
        "cart_items": cart_items,
        "total_price": total_price
    })


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Якщо користувач авторизований — перевірити, що це його замовлення
    if request.user.is_authenticated and order.user != request.user:
        return redirect('kabinet')

    if order.status == 'active':
        order.status = 'cancelled'
        order.save()

    return redirect('kabinet')
