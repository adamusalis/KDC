from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the VTU Site Backend! The API is running.")