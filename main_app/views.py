from django.shortcuts import render


# Create your views here.
def index(request):
    # return HttpResponse('base Karol!')
    return render(request, "home.html")


def displayFormErrors(form):
    print('Invalid form')
    print('reasons: ')
    for reason in form.errors:
        print(reason)
        for error in form.errors[reason]:
            print(error)
