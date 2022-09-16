from django.shortcuts import render
from django.views import View
from .models import *

class ProductView(View):
    def get(self, request):
        return render(request, "products/products.html", {'categories': Category.objects.all()})
