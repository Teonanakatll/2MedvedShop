from .views import product

from django.urls import path


urlpatterns = [
    path('product/<int:product_id>/', product, name='product'),
]