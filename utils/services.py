from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.requests import RequestSite


def send_email_to_verify(request, user):
    current_site = RequestSite(request)
    print('!', current_site)
    context = {
        'user':user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': request.scheme,
    }

    message = render_to_string('registration/verify_your_email.html', context=context)

    email = EmailMessage('Verify your email', message, to=[user.email])

    email.send()




    