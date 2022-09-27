from django import forms
from django.forms import inlineformset_factory

from products.models import CategoryAttribute, Category


class CategoryAttributeForm(forms.ModelForm):
    class Meta():
        model = CategoryAttribute
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['show_on_tile'].widget.attrs['class'] = 'form-check-input'
        self.fields['show_in_description'].widget.attrs['class'] = 'form-check-input'
        self.fields['filter_type'].widget.attrs['class'] = 'form-select'


CategoryAttributeFormSet = inlineformset_factory(Category, CategoryAttribute, form=CategoryAttributeForm, extra=0, can_delete=True)


class CategoryEditForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = ['name', 'parent']


    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['name'].widget.attrs['class'] = 'form-control'
            self.fields['parent'].widget.attrs['class'] = 'form-select'