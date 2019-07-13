from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('superuser_required/', views.SuperuserRequired.as_view(), name="superuser_required"),
    path('verify_account/<uidb64>/<token>/', views.verify_account, name="verify_account"),
    # path('reset_password/', views.reset_password, name='reset_password')  # in default auth
]
