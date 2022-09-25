from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from functools import reduce
import operator


from .services import *
from .models import *


class ProductsFilterView(View):
    def get(self, request):
        
        path = request.path

        query = get_query(request.build_absolute_uri())
        print('!!!', query)
        sku_lst = StockKeepingUnit.objects.filter(query)

        print('!', sku_lst)


        
        # sku_ids = StockKeepingUnit.objects.filter(reduce(operator.or_, query))
        # print('!', sku_ids)


        # sku_ids = StockKeepingUnit.objects.filter(Q(
        #     skucategoryattribute__in=SKUCategoryAttribute.objects.filter(
        #         category_attribute=CategoryAttribute.objects.get(
        #             id=category_lst[0]['category_attr']), 
        #         value=category_lst[0]['param']))|Q())
        
        # print('!!', sku_ids)

        category_name = path.split('/')[-2]
        category = get_object_or_404(Category, name__iexact=category_name)
        
        sku_list = StockKeepingUnit.objects.filter(product__in=Product.objects.filter(category=category))
        
        category_attrs = CategoryAttribute.objects.filter(Q(category=category) | Q (category=category.parent))
        
        filters = get_filters(category_attrs, sku_list)
            
        context = {
            'sku_list': sku_lst,
            'category': category,
            'filters': filters,
        }
        
        return render(request, "products/products.html", context=context)
