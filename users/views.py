from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from allauth.account.views import LoginView, SignupView
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core.validators import validate_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


from .forms import *


class UserProfileView(View):
    pass


class MyAccountSignupView(SignupView):
    form_class = MyUserCreationForm


class RegisterView(View):
    def get(self, request):
        context = {
            "form": MyUserCreationForm()
        }
       
        return render(request, 'registration/register.html', context)


    def post(self, request):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
         
            
            send_email_to_verify(request, user)

            return redirect('users:confirm-email')


        context = {
            'form': form,
        }
        
        # return render(request, self.form, context=context)


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm    
    
    def form_invalid(self, form):
     
        if form.not_verified:
            return redirect('users:confirm-email')
        return super().form_invalid(form)

class RegistrationValidationView(View):
    def get(self, request):
        result = []
        email = request.GET.get('email_val')

        try:
            validate_email(email)
        except ValidationError as e:
            result.append('invalid email')
        
        
        if User.objects.filter(email=email).count() != 0:
            result.append('User with this address already exists')
        return JsonResponse({'result': result})



class LoginValidationView(View):
    def get(self, request):
        
        email = request.GET.get('email_val')
        password = request.GET.get('pass_val')

        user = authenticate(email=email, password=password)
        if user is not None:
            result = 'success'
        elif user is None:
            result = 'failed'
        
        return JsonResponse({'result': result})


class EmailVerificationView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        return redirect('users:invalid-email')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user
