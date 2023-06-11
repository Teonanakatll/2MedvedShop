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
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        # Если товар пользователь удаляет из корзины ставим is_active=False
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        # Возвращает обьект (ищет по совпадающим полям), или создаёт со всеми указанными полями
        # Метод возвращает добавленный обьект и буллевое значение (created) True если дабавление прошло успешно
        # Если обьектов больше одного вернет MultipleObjectsReturned
        # По полю nmb - ненужно искать совпадения, ном его нужно обновить, поэтому записываем его в "defaults"
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, is_active=True, product_id=product_id, defaults={"nmb": nmb})

        # Если запись уже существует обновляем количество товара
        if not created:
            print("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    #common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    # Создаём список для перерисовки товаров (через Ajax) в корзине,
    # после добавления нового или изменения количества товара
    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()                    # Создаём словарь для каждого товара
        product_dict["id"] = item.id             # id - для удаления товара через Ajax
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)


    return JsonResponse(return_dict)
