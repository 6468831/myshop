from django.template.loader import render_to_string
from django.db.models import Min, Max
from django.db.models import Q
from functools import reduce
import operator

from .models import *

# ---filter rendering---

# getting all filters rendered to string
def get_filters(category_attrs, sku_list):
    
    filters = []
    
    for category_attr in category_attrs:
        if category_attr.filter_type == 'range':
            filters.append(create_range_filter(category_attr, sku_list))
        else:
            # Multiple and single choice filters have same values to output.
            filters.append(create_choice_filter(category_attr, sku_list))
        
    return filters            
            

def create_range_filter(category_attr, sku_list):
    sku_category_attrs = get_sku_category_attrs(category_attr, sku_list)
    if sku_category_attrs.exists():
        filter = render_to_string(
            'products/__range_filter.html', 
            {
            'category_attr': category_attr.attribute.name,
            'category_id': category_attr.id,
            'units': category_attr.units,
            'min': sku_category_attrs.aggregate(value=Min('value')),
            'max': sku_category_attrs.aggregate(value=Max('value')),
        })
    else:
        filter = ''
    
    return filter


# creating single and multiple choice filters
def create_choice_filter(category_attr, sku_list):

    values = get_values_for_filters(category_attr, sku_list, category_attr.filter_type)
    template = 'products/__single_filter.html' if category_attr.filter_type == 'single' else 'products/__multi_filter.html'
    
    if values:
        filter = render_to_string(
            template,
            {
                'category_attr': category_attr.attribute.name,
                'category_id': category_attr.id,
                'units': category_attr.units,
                'values': values,
            }
        )
    else:
        filter = ''
    
    return filter
  
        
def get_sku_category_attrs(category_attr, sku_list):
    sku_category_attrs = SKUCategoryAttribute.objects.filter(
        category_attribute=category_attr,
        category_attribute__filter_type='range', 
        sku__in=sku_list)
    return sku_category_attrs 


# getting values for choice filters
def get_values_for_filters(category_attr, sku_list, filter_type):
    
    values = SKUCategoryAttribute.objects.filter(
        category_attribute=category_attr,
        category_attribute__filter_type=filter_type,
        sku__in=sku_list).values('value').distinct()
    
    return values
            
         
# ---filtering results---

def get_query(params_in_url):
    
    # Parsing parameters
    # Creating different types of dicts for each of 3 filter types 
    # Passing them into Q objects.
    # Merging Q objects into one.
    
    params = params_in_url.split('?')[1].split('&') if '?' in params_in_url else None
    
    query = Q()

    if params:
        for param in params:
            if param:
                param = param.split(',')
                filter_type = CategoryAttribute.objects.get(id=param[0]).filter_type
                if filter_type == 'single':
                    dicts = (
                        {'id': param[0]},
                        {'value': param[1]},
                    )
                    query &= create_q_object(dicts)
                
                elif filter_type == 'multi':
                    # create separate dict for each of chosen values
                    multi_queries = Q()
                    for value in param[1:]:
                        dicts = (
                            {'id': param[0]},
                            {'value': value},
                        )
                        multi_queries |= create_q_object(dicts)
                    query &= multi_queries
                
                elif filter_type == 'range':
                    # create greater than and lower than dicts if corresponding values exist
                    if param[1] != '':
                        dicts = (
                            {'id': param[0]},
                            {'value__gte': param[1]},
                        )
                        query &= create_q_object(dicts)
                    if param[2] != '':
                        dicts = (
                            {'id': param[0]},
                            {'value__lte': param[2]},
                        )
                        query &= create_q_object(dicts)
                    
    return query




def create_q_object(dicts):
    return Q(id__in=StockKeepingUnit.objects.filter(skucategoryattribute__in=SKUCategoryAttribute.objects.filter(
                category_attribute=CategoryAttribute.objects.get(
                    **dicts[0]), 
                **dicts[1])))

