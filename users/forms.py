from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError




from utils.services import send_email_to_verify

# UserModel = get_user_model()

User = get_user_model()


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "id": "sign-up-email"}),)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email']


class MyAuthenticationForm(AuthenticationForm):
    not_verified = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_verified:
            self.not_verified = True
            send_email_to_verify(self.request, user)

            raise ValidationError(self.error_messages['inactive'], code='not verified',)
            

class MyPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})