from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
# Create your views here.
def bug_report(request):
    # return HttpResponse('base Karol!')
    if request.method == "POST":
        msg = request.POST.get("message")
        if msg!= "":
            send_mail(
                'Bug Reported',
                msg,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return redirect('report/successful')
    return render(request, "bug_report.html")

def report_successful(request):
    # return HttpResponse('base Karol!')
    return render(request, "report_successful.html")