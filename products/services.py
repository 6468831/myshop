from django.template.loader import render_to_string
from django.db.models import Min, Max

from .models import *

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
            
         