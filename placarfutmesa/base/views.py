from django.http import HttpResponse


# Create your views here.
def home(request):
    return HttpResponse('<html><body>PLACAR - FUTEBOL DE MESA</html></body>', content_type='text/html')
