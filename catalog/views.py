from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from catalog.models import Product, Category
from catalog.services import get_products_by_category
import logging


logger = logging.getLogger(__name__)


class ProductListView(View):
    """
    Представление списка продуктов с низкоуровневым кэшированием
    """
    template_name = 'catalog/product_list.html'
    paginate_by = 10

    def get(self, request):
        page = request.GET.get('page', 1)
        cache_key = f"product_list_page_{page}"

        # Проверяем кэш
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.info(f"Список продуктов (страница {page}) получен из кэша")
            return render(request, self.template_name, cached_data)

        # Получаем продукты
        products = Product.objects.filter(is_published=True).select_related('category', 'owner').order_by('-creation_date')

        # Пагинация
        from django.core.paginator import Paginator
        paginator = Paginator(products, self.paginate_by)
        page_obj = paginator.get_page(page)

        # Подготавливаем контекст
        context = {
            'products': page_obj,
            'product_count': products.count(),
        }

        # Сохраняем в кэш на 5 минут
        cache.set(cache_key, context, timeout=300)
        logger.info(f"Список продуктов (страница {page}) сохранен в кэш: {len(page_obj)} продуктов")

        return render(request, self.template_name, context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список товаров'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')

        if not pk:
            raise Http404("Не указан ID продукта")

        cache_key = f'product_detail_{pk}'

        product = cache.get(cache_key)

        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(cache_key, product, settings.CACHE_TTL)

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['title'] = f'Товар: {product.name}'

        if self.request.user.is_authenticated:
            context['is_moderator'] = self.request.user.groups.filter(name='Модератор продуктов').exists()
        return context


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user or self.request.user.groups.filter(
            name='Модератор продуктов').exists()

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
        return product.owner == self.request.user or self.request.user.groups.filter(
            name='Модератор продуктов').exists()


@login_required
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.has_perm('catalog.can_unpublish_product') or request.user == product.owner:
        product.is_published = False
        product.save()
        # Очищаем кэш для этого продукта
        cache_key = f"product_detail_{pk}"
        cache.delete(cache_key)
        return redirect('catalog:product_detail', pk=product.pk)
    else:
        raise PermissionDenied


def category_product_list(request, category_id):
    """
    Отображает список продуктов в указанной категории.
    Использует сервисную функцию для получения данных.
    """
    category = get_object_or_404(Category, pk=category_id, is_active=True)
    products = get_products_by_category(category_id)

    context = {
        'category': category,
        'products': products,
        'title': f'Товары категории: {category.name}',
    }

    return render(request, 'catalog/category_product_list.html', context)

