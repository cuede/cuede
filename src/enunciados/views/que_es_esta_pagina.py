from django.shortcuts import get_object_or_404, render


def que_es_esta_pagina(request):
    return render(request, 'que_es_esta_pagina.html')
