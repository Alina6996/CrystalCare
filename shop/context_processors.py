def cart_context(request):
    cart_items = request.session.get('cart', [])
    total_price = sum(float(item['total_price']) for item in cart_items)
    return {
        'cart_items': cart_items,
        'total_price': total_price
    }