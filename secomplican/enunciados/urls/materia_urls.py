from django.urls import path, include

from enunciados.views import materias


urlpatterns = [
    path('', materias.materia, name='materia'),
    path('practicas/', include('enunciados.urls.practicas_urls')),
    path('parciales/',
         include('enunciados.urls.parciales_urls', namespace='parciales'),
         kwargs={'recuperatorio': False},
         ),
    path('recuperatorios/',
         include('enunciados.urls.parciales_urls', namespace='recuperatorios'),
         kwargs={'recuperatorio': True},
         ),
    path('finales/', include('enunciados.urls.finales_urls')),
]
