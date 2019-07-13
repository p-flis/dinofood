from accounts.forms import CustomUserCreationForm
from accounts.models import User
from django.shortcuts import render,redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
# from django.contrib.auth import views as auth_views


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

    def form_valid(self, form: CustomUserCreationForm):
        result = super().form_valid(form)

        if form.cleaned_data['email_verification']:
            user: User = form.instance
            user.is_active = False
            user.save()
            self.send_registration_email(user)
        else:
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"]
            )
            login(self.request, user)

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


class SuperuserRequired(generic.TemplateView):
    template_name = "superuser_required.html"


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'
INTERNAL_RESET_URL_TOKEN = 'set-password'


# todo can't login to mail
# class VerifyAccount(auth_views.PasswordResetConfirmView):
#     form_class = None
#     token_generator = default_token_generator
#     success_url = reverse_lazy('login')
#
#     def get(self, request, *args, **kwargs):
#         if self.validlink:
#             self.user.is_active = True
#             self.user.save()
#         return super().get(request, *args, **kwargs)


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
                return redirect(reverse('login'))
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
