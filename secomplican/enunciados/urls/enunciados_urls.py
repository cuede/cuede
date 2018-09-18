from django.urls import path, include

from enunciados.views.enunciados import ver, editar, versiones
from enunciados.views.soluciones import crear as crear_solucion


app_name = 'enunciados'

enunciado_urlpatterns = [
    path('', ver.enunciado, name='ver_enunciado'),
    path('editar/', editar.enunciado, name='editar_enunciado'),
    path('versiones/', versiones.VersionesEnunciadoView.as_view(),
         name='versiones_enunciado'),
    path('nueva-solucion/', crear_solucion.CrearSolucion.as_view(),
         name='crear_solucion'),
]

urlpatterns = [
    path('<int:numero>/', include(enunciado_urlpatterns)),
]
