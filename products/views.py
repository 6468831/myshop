from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Q


from .services import *
from .models import *


class ProductsFilterView(View):
    def get(self, request):
        
        path = request.path

        category_name = path.split('/')[-2]
        category = get_object_or_404(Category, name__iexact=category_name)
        
        sku_list = StockKeepingUnit.objects.filter(product__in=Product.objects.filter(category=category))
        
        category_attrs = CategoryAttribute.objects.filter(Q(category=category) | Q (category=category.parent))
        
        filters = get_filters(category_attrs, sku_list)
            
        context = {
            'sku_list': sku_list,
            'category': category,
            'filters': filters,
        }
        
        return render(request, "products/products.html", context=context)
