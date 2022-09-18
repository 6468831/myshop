from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



from utils.services import send_email_to_verify

UserModel = get_user_model()

User = get_user_model()


class UserCreationForm(UserCreationForm):
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