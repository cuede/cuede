from django.http import HttpResponse
from django.shortcuts import render

import secomplican.settings as settings

def index(request):
    return render (request, 'index.html')
