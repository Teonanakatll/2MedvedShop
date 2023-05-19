from django.contrib import admin
from .models import Order, Status, ProductInOrder


class ProductInOrderInline(admin.TabularInline):
    """ inline-форма добавления связанной (ForeignKey) записи в БД. """
    model = ProductInOrder
    extra = 0

class StatusAdmin(admin.ModelAdmin):
    """ Отображение статуса в админ-панели. """
    list_display = [field.name for field in Status._meta.fields]


class OrderAdmin(admin.ModelAdmin):
    """ Отображение заказа в одмин-панели. """
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]


class ProductInOrderAdmin(admin.ModelAdmin):
    """ Отображение продукта относящегося к заказу в админ-панели. """
    list_display = [field.name for field in ProductInOrder._meta.fields]


admin.site.register(Order, OrderAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах'
