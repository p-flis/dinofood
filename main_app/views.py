from django.shortcuts import render


# Create your views here.
def index(request):
    # return HttpResponse('base Karol!')
    return render(request, "home.html")
