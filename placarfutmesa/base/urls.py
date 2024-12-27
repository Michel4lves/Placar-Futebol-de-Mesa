from django.urls import path

from placarfutmesa.base.views import home


app_name = 'base'
urlpatterns = [
    path('', home, name='home'),
]
