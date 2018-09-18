from django.urls import path, include

from enunciados.views import conjuntos_de_enunciados

final_urlpatterns = [
    path('', conjuntos_de_enunciados.final, name='final'),
    path('', include('enunciados.urls.enunciados_urls',
                     namespace='enunciados_final')),
]

urlpatterns = [
    path('<int:anio>/<int:mes>/<int:dia>/', include(final_urlpatterns)),
]
