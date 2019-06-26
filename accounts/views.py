from accounts.forms import CustomUserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import PasswordResetForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def superuser_required(request):
    return render(request, "superuser_required.html")


# in default auth.....
# def reset_password(request):
#     if request.method == 'GET':
#         form = PasswordResetForm()
#         return render(request, "reset_password.html", context={'form': form})
#     elif request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             form.save(
#                 request=request,
#                 email_template_name='registration/password_reset_email.html'
#             )
#         form = PasswordResetForm()
#         return render(request, "reset_password.html", context={'form': form, 'link_sent': True})
