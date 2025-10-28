from django.urls import path
from . import views

urlpatterns = [
    path('registraciya/', views.registraciya, name='registraciya'),
    path('vhid/', views.vhid, name='vhid'),
    path('kabinet/', views.kabinet, name='kabinet'),
    path('logout/', views.user_logout, name='logout'),
]