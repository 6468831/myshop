from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.template.loader import render_to_string
from django.db.models import Min, Max

from .models import *


class ProductsFilterView(View):
    def get(self, request):
        path = request.path

        category_name = path.split('/')[-2]
        category = get_object_or_404(Category, name__iexact=category_name)
        products = Product.objects.filter(category=category)
        
        filters = []
        for category_attr in CategoryAttribute.objects.filter(Q(category=category) | Q (category=category.parent)):
            print('!', ProductCategoryAttribute.objects.filter(
                category_attribute=category_attr,
                category_attribute__filter_type='range', 
                product__in=products).
                aggregate(Max('value')))
            print(products.aggregate(Max('productcategoryattribute__value')))

            if category_attr.filter_type == 'range':
                filter = render_to_string(
                    'products/__range_filter.html', 
                    {
                    'category_attr': category_attr.attribute.name,
                    'min': ProductCategoryAttribute.objects.filter(
                        category_attribute=category_attr,
                        category_attribute__filter_type='range', 
                        product__in=products).
                        aggregate(value=Min('value')),
                    'max': ProductCategoryAttribute.objects.filter(
                        category_attribute=category_attr,
                        category_attribute__filter_type='range', 
                        product__in=products).
                        aggregate(value=Max('value')),
                })
                filters.append(filter)
            elif category_attr.filter_type == 'multi':
                filter = render_to_string(
                    'products/__multi_filter.html',
                    {
                    
                    }
                )
                
            

        context = {
            'products': products,
            'category': category,
            'filters': filters,
        }
        
        return render(request, "products/products.html", context=context)
