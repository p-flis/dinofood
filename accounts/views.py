from accounts.forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def superuser_required(request):
    return render(request, "superuser_required.html")
