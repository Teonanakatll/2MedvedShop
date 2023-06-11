// Инициируем обёртку jquery после загрузки html-документа
$(document).ready(function(){
    // Создаём переменную,
    // $ значит к этому элементу страницы абращаемся как к элементу jquery
    // # выбираем элемент по id
    var form = $('#form_buying_product');
    // Вывадим в консоль
    console.log(form);

// ФУНКЦИЯ РАБОТАЕТ С БД ЧЕРЕЗ basket_adding, ПРИНИМАЕТ КВЕРИСЕТ ПО КЛЮЧУ СЕССИИ ДЛЯ ОТРИСОВКИ В КОРЗИНЕ,
// ПЕРЕДАЁТ ДАННЫЕ В basket_adding ДЛЯ ДОБАВЛЕНИЯ ЗАПИСИ В БД ProductInBasket,
// УДАЛЯЕТ ЗАПИСЬ ИЗ БД. (ВСЁ ЭТО БЕЗ ПЕРЕЗАГРУЗКИ СТРАНИЦЫ)

    function basketUpdating(product_id, nmb, is_delete){
        // добавить или изменить значение атрибута data у всех выбранных элементов
        //$('селектор').attr('data-*','значение');

        // В славаре data будут данные которые мы будем использовать для добавления модели ProductInBasket
        // и после удачного добавления записи в бд, для добавления выбранного товара и его кол-ва в корзину
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;

        // В переменную csrf_token добавляем токен (из формы), который нужен джанго чтобы отправить post-запрос
        var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        // Добавляем токен в славарь data
        data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete){
            data["is_delete"] = true;
        }

        // Адрес на который необходимо отпоавлять post-запрос
        // url считываем с аттрибута action на форме
        var url = form.attr("action");

        console.log(data);

        $.ajax({
            url: url,
            type: 'POST',
            data: data,   // Переменная с донными
            cache: true,
            success: function(data) {  // При успешном ответе сервера вызывается функция
                console.log("OK");
                // Выводим в консоль данные переменной products_total_nmb, переданные функцией представления adding_basket
                console.log(data.products_total_nmb);
                // Если есть, отрисовываем в корзине количество позиций товаров, текстом в span
                if (data.products_total_nmb || data.products_total_nmb == 0) {
                    $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                    // Выводим данные JsonResponse переданные с бэкэнда (views, basket_adding)
                    console.log(data.products);
                    // Очищаем предыдущие записи (ul) в корзине перед перерисовкой
                    $('.basket-items ul').html("");
                    $.each(data.products, function(k, v) {
                        // Обращаемся к елементу на уровень ниже (ul)
                        // И с помощю функции append() добавляем в него элемент
                        $('.basket-items ul').append('<li>'+v.name+', '+ v.nmb + 'шт. ' + 'по ' + v.price_per_item + 'руб.' +
                        // Чтоб появился курсор добавляем href=""
                        // Добавляем 'x' и дата-аттрибут data-product_id для возм. удаления
                        '<a href="" class="delete-item" data-product_id="'+v.id+'">x</a>'+
                        '</li>');
                    })
                }

            },
            error: function() {
                console.log("error")   // При ошибке
            }
        })
    }

    //      ФУНКЦИЯ ОТРАБАТЫВАЕТ ПРИ НАЖАТИИ НА КНОПКУ 'Купить' НА ТОВАРЕ В product.html

    // Присоединяем к форме событие, при событии передаём функции параметр е (event) - cтандартвый
    // евент отправки формы
    form.on('submit', function(e){
        // прмменяем к е функцмю preverntDefault(), которая отменяет стандартное поведение
        // евента (чтобы форма не отправлялась)
        e.preventDefault();
        console.log('123');
        // Создаём переменную nmb
        // По id или name, вызываем элемент input формы и с помощю .val() берем его значение
        var nmb = $('#num').val();
        console.log(nmb);
        // Создаём переменную с id кнопки
        var submit_btn = $('#submit_btn');
        // Обращаемся к переменной кнопки и с помощью ф. .data() берем data атрибуты и
        // присваиваем их значения переменным
        var product_id = submit_btn.data("product_id");
        var product_name = submit_btn.data("product_name");
        var product_price = submit_btn.data("product_price");
        console.log(product_id);
        console.log(product_name);
        console.log(product_price);

        basketUpdating(product_id, nmb, is_delete=false)

    });

    // Написоние функции (дублирование кода)
    function showingBasket(){
//        $('.basket-items').removeClass('visually-hidden');
        // toglleClass - если есть класс убирает его и на оборот
        $('.basket-items').removeClass('visually-hidden');
    };

    // ПО КЛИКУ НА .basket-container
    $('.basket-container').on('click', function(e){
        e.preventDefault();
        showingBasket();
    });
    // ПРИ НАВЕДЕНИИ МЫШИ
    $('.basket-container').mouseover(function(){
        showingBasket();
    });
    // ПРИ ОТВОДЕ МЫШИ ДОБАВЛЯЕТ КЛАСС visually-hidden
//    $('.basket-container').mouseout(function(){
//        $('.basket-items').addClass('visually-hidden');
//        showingBasket()
//    });

    // ПО КЛИКУ НА КРЕСТИК
    // Чтобы удалить из корзины товар через класс delete-item который был созданн
    // после дабавления товара, необходимо снова обратиться через $(document)
    // так как этот элемент создан после загрузки страницы и jquery не знает о его существовании
    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        // product_id будем считывать с дата атрибута кнопки
        product_id = $(this).data("product_id");
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true)
//        // Обращаемся к этому же елементу через (this), и выбираем ближайший к нему элемент li
//        $(this).closest('li').remove();
    })

});