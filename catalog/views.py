from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.models import Product
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    #Декоратор на основе класса
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'  # Шаблон для создания товара
    success_url = reverse_lazy('catalog:product_list')  # Перенаправление после успешного создания

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца продукта
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        # Доступ разрешен владельцу или модератору
        return product.owner == self.request.user or self.request.user.groups.filter(name='Модератор продуктов').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_moderator'] = self.request.user.groups.filter(name='Модератор продуктов').exists()
        return context


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        # Доступ разрешен владельцу или модератору
        return product.owner == self.request.user or self.request.user.groups.filter(name='Модератор продуктов').exists()


@login_required
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.has_perm('catalog.can_unpublish_product') or request.user == product.owner:
        product.is_published = False
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)
    else:
        raise PermissionDenied
