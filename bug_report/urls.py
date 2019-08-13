from django.urls import path

from . import views


urlpatterns = [
    path("report", views.BugReport.as_view(), name="bug_report"),
    path("report/successful", views.ReportSuccessful.as_view(), name="bug_report_successful"),
]
