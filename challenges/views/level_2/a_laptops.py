"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, HttpResponse, JsonResponse

from challenges.models import Laptop


def laptop_details_view(request: HttpRequest, laptop_id: int) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    try:
        laptop = Laptop.objects.get(id=laptop_id)
    except Laptop.DoesNotExist:
        return HttpResponse('Ноутбук с данным ID отсутствует в БД', status=404)
    return JsonResponse(
        data=laptop.to_json(),
        content_type='application/json; charset=utf-8',
    )


def laptop_in_stock_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops = Laptop.objects.filter(stock__gt=0).order_by('-created_at')
    laptops_json = list(map(Laptop.to_json, laptops))
    if laptops_json:
        return JsonResponse(
            data=laptops_json,
            safe=False,
            content_type='application/json; charset=utf-8',
        )
    return HttpResponse('На складе нет ноутбуков')


def laptop_filter_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    valid_brands = [choice[0].lower() for choice in Laptop._meta.get_field('brand').choices]
    brand = request.GET.get('brand', '').lower()
    min_price = int(request.GET.get('min_price', -1))
    if brand not in valid_brands or min_price < 0:
        return HttpResponse('Некорректные параметры фильтров', status=403)

    laptops = Laptop.objects.filter(brand__iexact=brand, price__gte=min_price).order_by('price')
    laptops_json = list(map(Laptop.to_json, laptops))
    if laptops_json:
        return JsonResponse(
            data=laptops_json,
            safe=False,
            content_type='application/json; charset=utf-8',
        )
    return HttpResponse('По заданным фильтрам ничего не найдено')


def last_laptop_details_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    laptop = Laptop.objects.latest()
    if laptop:
        return JsonResponse(
            data=laptop.to_json(),
            content_type='application/json; charset=utf-8',
        )
    return HttpResponse('Отсутствуют данные', status=404)
