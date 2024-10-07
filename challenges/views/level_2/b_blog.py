"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from datetime import timedelta

from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone

from challenges.models import Post


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    posts = Post.objects.filter(status='published').order_by('-published_at')[:3]
    posts_json = list(map(Post.to_json, posts))
    if posts_json:
        return JsonResponse(
            data=posts_json,
            safe=False,
            content_type='application/json; charset=utf-8',
            )
    return HttpResponse('Никто не публиковал посты :(')


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    query = request.GET.get('q')
    if query is None:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )
    posts_json = list(map(Post.to_json, posts))
    if posts_json:
        return JsonResponse(
            data=posts_json,
            safe=False,
            content_type='application/json; charset=utf-8',
            )
    return HttpResponse('По Вашему запросу ничего не найдено')


def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = Post.objects.filter(category__isnull=True).order_by('author', 'created_at')
    posts_json = list(map(Post.to_json, posts))
    if posts_json:
        return JsonResponse(
            data=posts_json,
            safe=False,
            content_type='application/json; charset=utf-8',
            )
    return HttpResponse('В данной категории посты отсутствуют')


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories = request.GET.get('categories')
    if categories:
        posts = Post.objects.filter(category__in=categories.lower().split(','))
    else:
        posts = Post.objects.filter(category__isnull=True)
    posts_json = list(map(Post.to_json, posts))
    if posts_json:
        return JsonResponse(
            data=posts_json,
            safe=False,
            content_type='application/json; charset=utf-8',
            )
    return HttpResponse('По Вашему запросу ничего не найдено')


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    last_days = request.GET.get('last_days')
    if last_days and last_days.isdigit():
        date = timezone.now().date() - timedelta(days=abs(int(last_days)))
        posts = Post.objects.filter(published_at__gte=date)
    else:
        return HttpResponse('Введите целое количество дней (last_days=5)', status=403)
    posts_json = list(map(Post.to_json, posts))
    if posts_json:
        return JsonResponse(
            data=posts_json,
            safe=False,
            content_type='application/json; charset=utf-8',
            )
