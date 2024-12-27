# from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    # return HttpResponse('<html><body>PLACAR - FUTEBOL DE MESA</html></body>', content_type='text/html')
    return render(request, 'base/home.html')
