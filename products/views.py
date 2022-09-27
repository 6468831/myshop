from django.shortcuts import render
from django.views import View
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy

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




class CategoryEditView(UpdateView):

    model = Category
    template_name = 'admin/admin_edit_category.html'
    form_class = CategoryEditForm


    def get_object(self, queryset=None):
        path = self.request.path
        
        category_name = path.split('/')[-2]
        category = get_object_or_404(Category, name__iexact=category_name)
        return category

    def get_success_url(self):
        return self.request.path
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        # passing user job experiences
        if self.request.POST:
            context['category_attrs_forms'] = CategoryAttributeFormSet(self.request.POST, instance=self.object)
            context['category_attrs_forms'].full_clean()
        else:
            context['category_attrs_forms'] = CategoryAttributeFormSet(instance=self.object)
          
        return context

    
    def form_valid(self, form):
        print('! here')
        context = self.get_context_data(form=form)

        formset = context['category_attrs_forms']
        print('!', formset.errors)

        if formset.is_valid():
            print('! form is valid')
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            print('! form is not valid')
            return super().form_invalid(form)