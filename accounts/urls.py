from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('superuser_required/', views.superuser_required, name="superuser_required")
]
