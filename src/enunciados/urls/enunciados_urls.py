from django.urls import include, path

from enunciados.views.enunciados import crear, editar, ver, versiones
from enunciados.views.soluciones import crear as crear_solucion
from enunciados.views.soluciones import editar as editar_solucion
from enunciados.views.soluciones import versiones as versiones_solucion

app_name = 'enunciados'

soluciones_urlpatterns = [
    path('editar/', editar_solucion.editar_solucion, name='editar_solucion'),
    path(
        'versiones/',
        versiones_solucion.VersionesSolucionView.as_view(),
        name='versiones_solucion'
    ),
]

enunciado_urlpatterns = [
    path('', ver.enunciado, name='ver_enunciado'),
    path('editar/', editar.enunciado, name='editar_enunciado'),
    path(
        'versiones/',
        versiones.VersionesEnunciadoView.as_view(),
        name='versiones_enunciado'
    ),
    path(
        'nueva-solucion/',
        crear_solucion.CrearSolucion.as_view(),
        name='crear_solucion'
    ),
    path('soluciones/<int:pk_solucion>/', include(soluciones_urlpatterns)),
]

urlpatterns = [
    path('<int:numero>/', include(enunciado_urlpatterns)),
    path('nuevo-ejercicio/', crear.nuevo_enunciado, name='nuevo_enunciado')
]
