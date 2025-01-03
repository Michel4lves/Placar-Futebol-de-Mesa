# from django.http import HttpResponse
from django.shortcuts import render


class Competition:
    def __init__(self, comp_id, comp_type, comp_name, comp_stage, comp_modality, comp_status):
        self.slug = "".join(comp_name.split())
        self.comp_id = comp_id
        self.comp_type = comp_type
        self.comp_name = comp_name
        self.comp_stage = comp_stage
        self.comp_modality = comp_modality
        self.comp_status = comp_status


competitions = [
        Competition(
            20250319,
            'Campeonato',
            'Campeonato interno',
            'Etapa 2',
            'Cavado',
            'Progress'
        ),
        Competition(
            20250410,
            'Copa',
            'Copa COP',
            '',
            'Cavado',
            'Progress'
        ),
        Competition(
            20250205,
            'Copa',
            'Circulão',
            '',
            'Cavado',
            'Closed'
        ),
]


# Create your views here.
def home(request):
    # return HttpResponse('<html><body>PLACAR - FUTEBOL DE MESA</html></body>', content_type='text/html')
    return render(request, 'base/home.html', context={'competitions': competitions})
