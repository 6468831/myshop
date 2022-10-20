import csv

from django.shortcuts import render
from django.views import View
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.files.storage import default_storage

from .services import *
from .models import *
from .forms import *


class ProductsFilterView(View):
    def get(self, request):
        
        path = request.path

        query = get_query(request.build_absolute_uri())
        print('!!!', query)
        
        category_name = path.split('/')[-2]
        category = get_object_or_404(Category, name__iexact=category_name)
        sku_list_for_filters = StockKeepingUnit.objects.filter(product__in=Product.objects.filter(category=category))
        sku_lst = StockKeepingUnit.objects.filter(query, product__in=Product.objects.filter(category=category))

        print('!', sku_lst)

        
        category_attrs = CategoryAttribute.objects.filter(Q(category=category) | Q (category=category.parent))
        
        # use sku_lst here to see only available filters
        filters = get_filters(category_attrs, sku_list_for_filters)
            
        context = {
            'sku_list': sku_lst,
            'category': category,
            'filters': filters,
        }
        
        return render(request, "products/products.html", context=context)



