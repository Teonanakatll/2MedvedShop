from django.shortcuts import render
from .models import Product


def product(request, product_id):
    """ Страница отображения товара. """
    product = Product.objects.get(id=product_id)
    return render(request, 'products/product.html', locals())
