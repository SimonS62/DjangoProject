from django.urls import path
from . import views  # Импортируем представления (контроллеры)


urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('contacts/', views.contacts, name='contacts'), #страница контактов
]
