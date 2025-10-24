from django.urls import path
from . import views

urlpatterns = [
    path('', views.katalog, name='katalog'),  # Каталог
    path('cart/', views.cart, name='cart'),   # Кошик
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Додати товар
    path('remove/<int:index>/', views.remove_from_cart, name='remove_from_cart'), # Видалити товар
    path('clear/', views.clear_cart, name='clear_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('catalog/', views.katalog, name='katalog'),
    path('catalog/<slug:category_slug>/', views.katalog, name='katalog_by_category'),
]
