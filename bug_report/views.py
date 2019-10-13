from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import django.views.generic as generic


def bug_report(request):
    if request.method == "POST":
        msg = request.POST.get("message")
        if msg != "":
            send_mail(
                'Bug Reported',
                msg,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return redirect('report/successful')
    return render(request, "bug_report.html")


class ReportSuccessful(generic.TemplateView):
    template_name = "report_successful.html"

