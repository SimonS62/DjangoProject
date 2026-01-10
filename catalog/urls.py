from django.urls import path
from .views import ContactsView, home, product_detail

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]
