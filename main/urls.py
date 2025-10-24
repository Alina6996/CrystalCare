from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('pro_nas/', views.pro_nas, name='pro_nas'),
    path('kontakty/', views.kontakty, name='kontakty'),
]