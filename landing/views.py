from django.shortcuts import render

from products.models import Product, ProductImage
from .forms import SubscriberForm


def landing(request):
    form = SubscriberForm(request.POST or None)

    # cleaned_data можно получить только после проверки is_valid()
    if request.method == "POST" and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)
        data = form.cleaned_data
        print(data["name"])

        form.save()
    return render(request, 'landing/landing.html', locals())


def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True)
    return render(request, 'landing/home.html', locals())
