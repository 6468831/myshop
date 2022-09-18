from django.urls import path
from .views import *


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile')
]