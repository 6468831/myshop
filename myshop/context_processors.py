from users.forms import MyUserCreationForm, MyAuthenticationForm, MyPasswordResetForm


def sign_up_form(request):
    return {
        'sign_up_form' : MyUserCreationForm()
    }


def sign_in_form(request):
    return {
        'sign_in_form' : MyAuthenticationForm()
    }


def password_reset_form(request):
    return {
        'password_reset_form' : MyPasswordResetForm()
    }


