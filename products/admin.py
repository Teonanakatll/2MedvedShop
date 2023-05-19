from django.contrib import admin

from products.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """ inline-форма добавления связанной (ForeignKey) записи в БД. """
    model = ProductImage
    # Кол-во inline-форм в админ-панели для модели.
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    """ Отображение продукта в админ-панели. """
    list_display = [field.name for field in Product._meta.fields]
    # Добавляем inline-форму к модели
    inlines = [ProductImageInline]


class ProductImageAdmin(admin.ModelAdmin):
    """ Отображение фотаграфии продукта в админ понели. """
    list_display = [field.name for field in ProductImage._meta.fields]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
