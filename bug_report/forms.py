from django import forms


class BugReportForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)