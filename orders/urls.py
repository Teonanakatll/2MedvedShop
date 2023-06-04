from django.urls import path

from orders.views import basket_adding


urlpatterns = [
    path('basket_adding/', basket_adding, name='basket_adding')
]