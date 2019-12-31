from django.urls import include, path

from enunciados.views.posteos import votar

app_name = 'votos'

votos_urlpatterns = [
    path('arriba/', votar.VotarArribaView.as_view(), name='votar_arriba'),
    path('abajo/', votar.VotarAbajoView.as_view(), name='votar_abajo'),
    path('sacar/', votar.SacarVotoView.as_view(), name='sacar_voto'),
]

urlpatterns = [
    path('votos/', include(votos_urlpatterns)),
]