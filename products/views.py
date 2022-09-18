from django.shortcuts import render
from django.views import View
from .models import *


class ProductsFilterView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products/products.html', {'products': products})
        # return render(request, "products/products.html", {'categories': Category.objects.all()})
