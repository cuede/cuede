from django.urls import include, path

from enunciados.views.soluciones import votar

app_name = 'soluciones'

votos_urlpatterns = [
    path('arriba/', votar.VotarArribaView.as_view(), name='votar_arriba'),
    path('abajo/', votar.VotarAbajoView.as_view(), name='votar_abajo'),
    path('sacar/', votar.SacarVotoView.as_view(), name='sacar_voto'),
]

urlpatterns = [
    path('votos/', include(votos_urlpatterns)),
]