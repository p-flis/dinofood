from django.shortcuts import render

# Create your views here.
def bug_report(request):
    # return HttpResponse('base Karol!')
    return render(request, "bug_report.html")