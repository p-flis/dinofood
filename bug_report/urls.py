from django.urls import path

from . import views


urlpatterns = [
    path("report", views.bug_report, name="bug_report"),
    path("report/successful", views.ReportSuccessful.as_view(), name="report_successful"),
]
