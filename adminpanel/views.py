from django.shortcuts import render
from django.views import View
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404

from products.models import Category, FileUpload
from .forms import *

class CategoryEditView(UpdateView):

    model = Category
    template_name = 'adminpanel/admin_edit_category.html'
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


class ImportFileDataView(View):
    def get(self, request):
        file = FileUpload.objects.last()
        print('!', file)
        # f = default_storage.open(os.path.join('Data_Files', new_file), 'r')
        # data = f.read()
        # f.close()
        # print(data)

        return render(request, 'products/file_upload.html')