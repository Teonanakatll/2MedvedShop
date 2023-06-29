from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from products.models import Product


class Status(models.Model):
    """ Модель статуса заказа. """
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    """ Модель с данными заказа. """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total price for all products in order
    customer_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=64, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Заказ %s %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        """ Переопределяем метод save() """
        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    """ Модель с донными продукта находящегося в зказе. """
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price * nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        """ Переопределяем метод save() """
        price_per_item = self.product.price
        self.price_per_item = price_per_item

        self.total_price = int(self.nmb) * price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)

# Функция post_save(), служит для изменения (пересчёта) зночений полей связанной (первичной) модели,
# при создании каждой связанной (вторичной) модели, используя зночения её полей.
# Изменять с помощью post_save() можно только поля в другой модели, попытка сохранить в тойже модели
# будет снова вызывать post_save() (зациклит).
def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    # Считываем все товары в заказе
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    # Проходим циклом по списку товаров и высяитываем общую стоимость
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        """ Переопределяем метод save() """
        price_per_item = self.product.price
        self.price_per_item = price_per_item

        self.total_price = int(self.nmb) * price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)
