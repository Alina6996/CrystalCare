from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile as AccountsProfile
from shop.models import Profile as ShopProfile, Order
from datetime import datetime

# -------------------- Реєстрація --------------------
def registraciya(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        birth_date_str = request.POST.get('birth_date', '')
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Паролі не співпадають!')
            return redirect('registraciya')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Користувач з таким ім’ям вже існує!')
            return redirect('registraciya')

        # Створюємо користувача
        user = User.objects.create_user(username=username, email=email, password=password1)

        # Створюємо обидва профілі
        accounts_profile, _ = AccountsProfile.objects.get_or_create(user=user)
        shop_profile, _ = ShopProfile.objects.get_or_create(user=user)

        # Заповнюємо дані акаунтс профілю
        accounts_profile.phone = phone
        if birth_date_str:
            try:
                accounts_profile.birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, 'Невірний формат дати народження')
        accounts_profile.save()

        login(request, user)
        return redirect('kabinet')

    return render(request, 'accounts/registraciya.html')


# -------------------- Вхід --------------------
def vhid(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Гарантуємо, що обидва профілі існують
            AccountsProfile.objects.get_or_create(user=user)
            ShopProfile.objects.get_or_create(user=user)

            login(request, user)
            return redirect('kabinet')
        else:
            messages.error(request, 'Невірний логін або пароль')
            return redirect('vhid')

    return render(request, 'accounts/vhid.html')


# -------------------- Кабінет --------------------
@login_required
def kabinet(request):
    # Беремо акаунтс профіль
    accounts_profile, _ = AccountsProfile.objects.get_or_create(user=request.user)
    # Беремо shop профіль (якщо потрібен)
    shop_profile, _ = ShopProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        accounts_profile.full_name = request.POST.get("full_name", "")
        accounts_profile.phone = request.POST.get("phone", "")
        birth_date_str = request.POST.get("birth_date")
        if birth_date_str:
            try:
                accounts_profile.birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Невірний формат дати народження")
        accounts_profile.address = request.POST.get("address", "")
        accounts_profile.promo_code = request.POST.get("promo_code", "")
        accounts_profile.save()
        messages.success(request, "Дані оновлено!")
        return redirect("kabinet")

    # Історія замовлень
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "accounts/kabinet.html", {
        "profile": accounts_profile,
        "orders": orders
    })


# -------------------- Вихід --------------------
@login_required
def user_logout(request):
    logout(request)
    return redirect('vhid')
