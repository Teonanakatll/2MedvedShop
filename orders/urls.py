from django.urls import path

from orders.views import basket_adding, checkout

urlpatterns = [
    path('basket_adding/', basket_adding, name='basket_adding'),
    path('checkout/', checkout, name='checkout'),
]