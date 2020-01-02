from http import HTTPStatus
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db.models import F
from django.views import View
from django.contrib.auth.decorators import login_required

from enunciados.utils import enunciados_url_parser
from enunciados.models import Voto, Solucion


PUNTOS_USUARIO_POR_VOTO = 10


def get_object_or_none(model, **kwargs):
    return model.objects.filter(**kwargs).first()


def sumar_puntos_a_creador(solucion, puntos):
    informacion_creador = solucion.creador.informacionusuario
    informacion_creador.puntos = F('puntos') + puntos
    informacion_creador.save()


def sumar_puntos_a_solucion(solucion, puntos):
    sumar_puntos_a_creador(solucion, puntos * PUNTOS_USUARIO_POR_VOTO)
    solucion.puntos = F('puntos') + puntos
    solucion.save()


class VotarView(View):
    def procesar_voto(self, usuario, voto, solucion):
        pass

    def post(self, request, *args, **kwargs):
        usuario = request.user
        if not usuario.is_authenticated:
            return HttpResponse('Unauthorized', status=HTTPStatus.UNAUTHORIZED)

        solucion = get_object_or_404(Solucion, id=kwargs['id_solucion'])
        voto = get_object_or_none(
            Voto,
            usuario=usuario.informacionusuario, solucion=solucion
        )

        self.procesar_voto(usuario, voto, solucion)

        return HttpResponse()


class AgregarVotoView(VotarView):
    def procesar_voto(self, usuario, voto, solucion):
        if not voto or voto.positivo != self.positivo:
            sumado = self.cambio_puntos
            if voto:
                sumado *= 2
                voto.positivo = self.positivo
            else:
                voto = Voto(
                    usuario=usuario.informacionusuario,
                    solucion=solucion,
                    positivo=self.positivo
                )
            if solucion.puntos + sumado >= 0:
                sumar_puntos_a_solucion(solucion, sumado)
                voto.save()


class VotarArribaView(AgregarVotoView):
    cambio_puntos = 1
    positivo = True


class VotarAbajoView(AgregarVotoView):
    cambio_puntos = -1
    positivo = False


class SacarVotoView(VotarView):
    def procesar_voto(self, usuario, voto, solucion):
        if voto:
            if voto.positivo:
                sumado = -1
            else:
                sumado = 1

            sumar_puntos_a_solucion(solucion, sumado)
            voto.delete()
