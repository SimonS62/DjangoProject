from django.core.cache import cache
from catalog.models import Product
from django.db.models import Q
import logging


logger = logging.getLogger(__name__)

def get_products_by_category(category_id, published_only=True, limit=None):
    """
    Сервисная функция для получения продуктов по категории с кэшированием.

    Args:
        category_id (int): ID категории
        published_only (bool): Только опубликованные продукты
        limit (int, optional): Ограничение количества продуктов

    Returns:
        list: Список продуктов
    """
    # Формируем ключ кэша
    cache_key = f"category_products_{category_id}_{published_only}_{limit or 'none'}"

    # Проверяем кэш
    cached_products = cache.get(cache_key)
    if cached_products is not None:
        logger.info(f"Продукты для категории {category_id} получены из кэша")
        return cached_products

    # Формируем запрос
    queryset = Product.objects.filter(category_id=category_id)

    if published_only:
        queryset = queryset.filter(is_published=True)

    if limit:
        queryset = queryset[:limit]

    # Получаем продукты
    products = list(queryset.select_related('category', 'owner'))

    # Сохраняем в кэш на 10 минут
    cache.set(cache_key, products, timeout=600)
    logger.info(f"Продукты для категории {category_id} сохранены в кэш: {len(products)} продуктов")

    return products


def get_all_categories():
    """
    Получить все категории с кэшированием.

    Returns:
        list: Список категорий
    """
    cache_key = "all_categories"

    cached_categories = cache.get(cache_key)
    if cached_categories is not None:
        return cached_categories

    from catalog.models import Category
    categories = list(Category.objects.all())
    cache.set(cache_key, categories, timeout=3600)  # Кэш на час
    return categories


def search_products(query, published_only=True, limit=20):
    """
    Поиск продуктов по названию или описанию.

    Args:
        query (str): Поисковый запрос
        published_only (bool): Только опубликованные
        limit (int): Лимит результатов

    Returns:
        list: Найденные продукты
    """
    cache_key = f"search_products_{query}_{published_only}_{limit}"

    cached_results = cache.get(cache_key)
    if cached_results is not None:
        return cached_results

    queryset = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )

    if published_only:
        queryset = queryset.filter(is_published=True)

    products = list(queryset.select_related('category', 'owner')[:limit])

    cache.set(cache_key, products, timeout=300)  # Кэш на 5 минут для поиска
    return products
