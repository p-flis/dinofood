from django.core.mail import send_mail
from django.conf import settings
import django.views.generic as generic
from django.urls import reverse_lazy
import bug_report.forms


class BugReport(generic.FormView):
    form_class = bug_report.forms.BugReportForm
    success_url = reverse_lazy('bug_report_successful')

    def form_valid(self, form):
        msg = form.cleaned_data['message']
        if msg != "":
            send_mail(
                'Bug Reported',
                msg,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        return super().form_valid(form)


class ReportSuccessful(generic.TemplateView):
    template_name = "report_successful.html"

