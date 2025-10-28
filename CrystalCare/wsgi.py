"""
WSGI config for CrystalCare project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

# Указываем модуль настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CrystalCare.settings')

# Получаем WSGI приложение
application = get_wsgi_application()
