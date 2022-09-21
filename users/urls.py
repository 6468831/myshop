from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import *
from .views import *


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login-validation/', LoginValidationView.as_view(), name='login-validation'),
    path('registration-validation/', RegistrationValidationView.as_view(), name='registration-validation'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('confirm-email/', TemplateView.as_view(template_name='registration/confirm_email.html'), name='confirm-email'), # user will see this page after registration
    path('email-verification/<uidb64>/<token>', EmailVerificationView.as_view(), name='email-verification'), #link that user gets in email
    path('invalid_email', TemplateView.as_view(template_name='registration/invalid_email.html'), name='invalid-email'),
]