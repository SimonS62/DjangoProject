from django.shortcuts import render, redirect, get_object_or_404
import json
from datetime import datetime
from .models import Product


def contacts(request):
    """
    Обрабатывает форму контактов и сохраняет данные в JSON-файл.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        data = {
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'phone': phone,
            'message': message
        }

        try:
            with open('contacts.json', 'a', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            print(f"Ошибка при записи в файл: {e}")
            return render(request, 'catalog/contacts.html', {'error_message': 'Произошла ошибка при сохранении данных.'}) # Исправлен путь

        return redirect('home')

    return render(request, 'catalog/contacts.html')


def home(request):
    """
    Отображает главную страницу со списком товаров. Получает все товары из базы данных.
    """
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/home.html', context)


def product_detail(request, pk):
    """
    Отображает подробную информацию о конкретном товаре.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)
