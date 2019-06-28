from accounts.forms import CustomUserCreationForm
from accounts.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template import loader


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

    def form_valid(self, form):
        result = super().form_valid(form)

        # user = authenticate(
        #     username=form.cleaned_data["username"],
        #     password=form.cleaned_data["password1"]
        # )
        # login(self.request, user)

        user: User = form.instance
        user.is_active = False
        user.save()
        self.send_registration_email(self.request)

        return result

    def send_registration_email(self, user):
        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain

        context = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }

        subject = loader.render_to_string("registration/registration_email_subject.txt", context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string("registration/registration_email.html", context)

        user.email_user(subject, body, "dinofoodnotification@gmail.com")


def superuser_required(request):
    return render(request, "superuser_required.html")


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'
INTERNAL_RESET_URL_TOKEN = 'set-password'


def verify_account(request, uidb64, token):
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        user = None

    if user is not None:
        if token == INTERNAL_RESET_URL_TOKEN:
            session_token = request.session.get(INTERNAL_RESET_SESSION_TOKEN)
            if default_token_generator.check_token(user, session_token):
                # If the token is valid, display the password reset form.
                user.is_active = True
                user.save()

                # todo: immediately log in user?
                return render(request, 'registration/login.html')
        else:
            if default_token_generator.check_token(user, token):
                # Store the token in the session and redirect to the
                # password reset form at a URL without the token. That
                # avoids the possibility of leaking the token in the
                # HTTP Referer header.
                request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                redirect_url = request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                return HttpResponseRedirect(redirect_url)

    # user doesn't exist
    return Http404
