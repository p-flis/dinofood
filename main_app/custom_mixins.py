import django.contrib.auth.mixins as mixins
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views import generic
from django.db import models


class SuperuserRequiredMixin(mixins.UserPassesTestMixin):
    login_url = reverse_lazy('superuser_required')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return auth_views.redirect_to_login(self.request.get_full_path(),
                                            self.get_login_url(),
                                            self.get_redirect_field_name())
