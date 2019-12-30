from django.contrib.auth.decorators import login_required
from http import HTTPStatus
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db.models import F
from django.views import View

from enunciados.utils import enunciados_url_parser
from enunciados.models import VotoEnunciado


def get_or_none(model, **kwargs):
    return model.objects.filter(**kwargs).first()


class VotarView(View):
    def procesar_voto(self, usuario, voto, enunciado):
        pass

    def post(self, request, *args, **kwargs):
        usuario = request.user
        if not usuario.is_authenticated:
            return HttpResponse('Unauthorized', status=HTTPStatus.UNAUTHORIZED)

        enunciado = enunciados_url_parser.kwargs_a_enunciado(kwargs)
        voto = get_or_none(
            VotoEnunciado,
            usuario=usuario.informacionusuario, enunciado=enunciado
        )

        self.procesar_voto(usuario, voto, enunciado)

        return HttpResponse()


class AgregarVotoView(VotarView):
    def procesar_voto(self, usuario, voto, enunciado):
        if not voto or voto.positivo != self.positivo:
            sumado = self.cambio_puntos
            if voto:
                sumado *= 2
                voto.positivo = self.positivo
            else:
                voto = VotoEnunciado(
                    usuario=usuario.informacionusuario,
                    enunciado=enunciado,
                    positivo=self.positivo
                )
            enunciado.votos = F('votos') + sumado
            voto.save()
            enunciado.save()


class VotarArribaView(AgregarVotoView):
    cambio_puntos = 1
    positivo = True


class VotarAbajoView(AgregarVotoView):
    cambio_puntos = -1
    positivo = False


class SacarVotoView(VotarView):
    def procesar_voto(self, usuario, voto, enunciado):
        if voto:
            if voto.positivo:
                restado = 1
            else:
                restado = -1
            enunciado.votos = F('votos') - restado
            voto.delete()
            enunciado.save()
