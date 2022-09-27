from django.urls import path, re_path

from .views import *

urlpatterns = [
    re_path(r'edit-category', CategoryEditView.as_view(), name='edit-category'),
    path('file-upload', ImportFileDataView.as_view(), name='file-upload')
    ]