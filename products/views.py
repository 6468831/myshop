from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404

from .models import *


class ProductsFilterView(View):
    def get(self, request):
        path = request.path
        category_name = path.split('/')[-1]
        print('!!', category_name)
        # categories = Category.objects.all()
        category = get_object_or_404(Category, name__iexact=category_name)
        products = Product.objects.filter(category=category)


        context = {
            'products': products,
            'category': category,
        }
        
        return render(request, "products/products.html", context=context)
