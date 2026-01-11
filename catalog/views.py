from django.shortcuts import render,redirect
from django.views.generic import DetailView, ListView, View
import json
from datetime import datetime
from .models import Product


class ContactsView(View):
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
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
            context = {'error_message': 'Произошла ошибка при сохранении данных.'}
            return render(request, self.template_name, context)

        return redirect('home')


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'  # Передаем список продуктов в шаблон под именем 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'  # Один продукт передается в шаблон под именем 'product'
