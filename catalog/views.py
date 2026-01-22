from django.shortcuts import render,redirect
from django.views.generic import DetailView, ListView, View
import json
from datetime import datetime
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy


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


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm  # Используйте форму
    template_name = 'catalog/product_form.html'  # Форма для создания
    success_url = reverse_lazy('product_list')  # Перенаправление после успеха


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'  # Одна форма для создания и обновления
    success_url = reverse_lazy('product_list')  # Перенаправление


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')