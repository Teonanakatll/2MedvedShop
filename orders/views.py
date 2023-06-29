from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from orders.forms import CheckoutContactForm
from orders.models import ProductInBasket, ProductInOrder, Order


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
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, order__isnull=True, is_active=True, product_id=product_id, defaults={"nmb": nmb})

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


def checkout(request):
    """ Функция отрисовывает список товаров из корзины."""
    session_key = request.session.session_key
    # Выбираем товары в корзине по ключу сессии, исключая товары которые уже находятся в заказе (не null)
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        # Если форма прошла валидацию
        if form.is_valid():
            print("yes")
            data = request.POST
            # Чтобы небыло исключения берем name через get()
            name = data.get("name", "one")  # "one" - при отсутствии присваиваем любое значение
            # Присваиваем переменной phone и email телефон из пост-запроса
            phone = data["phone"]
            email = data["email"]
            # По номеру телефона ищем юзера в дб, или создаём нового
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name, "email": email})

            # Создаём заказ с данными юзера, устанавливаем статус
            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone,
                                         customer_email=email, status_id=1)

            # Считываем добавленные товары из корзины (словарь POST)
            for name, value in data.items():
                # Если переменная начинается с...
                if name.startswith("product_in_basket_"):
                    # Берем елемент с индексом 1
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    # Считываем обьект по id
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    # Возникла ошибка can't multiply sequence by non-int of type 'decimal.Decimal'
                    # проверяем значение поля value
                    print(type(value))
                    # Устанавливаем количество товара со страницы checkout.html (при изменении)
                    product_in_basket.nmb = value
                    # Прописываем заказ к товару в корзине
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    # Создаём продукт в заказе
                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price, order=order)

        else:
            print("no")

    return render(request, 'orders/checkout.html', locals())
