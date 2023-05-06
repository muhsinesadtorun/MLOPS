from django.shortcuts import render, HttpResponse

x=1
def home_view(request):
    return render(request, 'home.html')