
from http import HTTPStatus
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db.models import F
from django.views import View
from django.contrib.auth.decorators import login_required

from enunciados.utils import enunciados_url_parser
from enunciados.models import Voto, Posteo


def get_object_or_none(model, **kwargs):
    return model.objects.filter(**kwargs).first()


class VotarView(View):
    def procesar_voto(self, usuario, voto, posteo):
        pass

    def post(self, request, *args, **kwargs):
        usuario = request.user
        if not usuario.is_authenticated:
            return HttpResponse('Unauthorized', status=HTTPStatus.UNAUTHORIZED)

        posteo = get_object_or_404(Posteo, id=kwargs['id_posteo'])
        voto = get_object_or_none(
            Voto,
            usuario=usuario.informacionusuario, posteo=posteo
        )

        self.procesar_voto(usuario, voto, posteo)

        return HttpResponse()


class AgregarVotoView(VotarView):
    def procesar_voto(self, usuario, voto, posteo):
        if not voto or voto.positivo != self.positivo:
            sumado = self.cambio_puntos
            if voto:
                sumado *= 2
                voto.positivo = self.positivo
            else:
                voto = Voto(
                    usuario=usuario.informacionusuario,
                    posteo=posteo,
                    positivo=self.positivo
                )
            posteo.puntos = F('puntos') + sumado
            voto.save()
            posteo.save()


class VotarArribaView(AgregarVotoView):
    cambio_puntos = 1
    positivo = True


class VotarAbajoView(AgregarVotoView):
    cambio_puntos = -1
    positivo = False


class SacarVotoView(VotarView):
    def procesar_voto(self, usuario, voto, posteo):
        if voto:
            if voto.positivo:
                restado = 1
            else:
                restado = -1
            posteo.puntos = F('puntos') - restado
            voto.delete()
            posteo.save()
