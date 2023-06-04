from django.http import JsonResponse
from django.shortcuts import render

from orders.models import ProductInBasket


def basket_adding(request):
    """ Функция обрабатывает post-запросы формы product.html, отправленные аджаксом,
          добавляет запись с ключом сессии в таблицу ProductInBasket,
          и по ключу сессии возвращает количество добавленных позиций товаров
          для отрисовки его в корзине."""
    return_dict = dict()

                               #  ДАННЫЕ ПОЛУЧАЕМ ОТ ФРОНТЕНДА
    # Считываем ключ сессии
    session_key = request.session.session_key
    print(request.POST)

    # Присваиваем переменной data данные из запроса переданного аджаксом
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")

    new_product = ProductInBasket.objects.create(session_key=session_key, product_id=product_id, nmb=nmb)
    products_total_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["products_total_nmb"] = products_total_nmb
    return JsonResponse(return_dict)
