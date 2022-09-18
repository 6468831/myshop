from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductsFilterView.as_view(), name='products')
]