from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from enunciados.models import (
    Universidad, Carrera, Materia, MateriaCarrera, Practica, Enunciado, VersionTexto,
    get_sentinel_user
)
from enunciados.utils import enunciados_url_parser

NUMERO_ENUNCIADO = 1


class EditarEnunciadoTests(TestCase):
    def setUp(self):
        universidad = Universidad.objects.create(nombre='uba')
        carrera = Carrera.objects.create(
            nombre='Computación', slug='compu', universidad=universidad)
        materia = Materia.objects.create()
        self.materia_carrera = MateriaCarrera.objects.create(
            nombre='materia', slug='materia', carrera=carrera, materia=materia
        )
        self.practica = Practica.objects.create(
            materia=materia, anio=2018, cuatrimestre=1, numero=1
        )
        self.enunciado = self.crear_enunciado_con_texto(NUMERO_ENUNCIADO)
        self.version_texto = self.enunciado.versiones.ultima()

    def crear_enunciado_con_texto(self, numero):
        enunciado = Enunciado.objects.create(conjunto=self.practica, numero=numero)
        VersionTexto.versiones.create(texto='hola', posteo=enunciado, autor=get_sentinel_user())
        return enunciado

    def url_editar_enunciado(self, numero=NUMERO_ENUNCIADO):
        return reverse('materia:practicas:practica:enunciados:editar_enunciado', kwargs={
            'materia_carrera': self.materia_carrera,
            'anio': 2018,
            'cuatrimestre': 1,
            'numero_practica': 1,
            'numero': numero,
        })

    def test_editar_enunciado_redirecciona_a_ver_enunciado(self):
        url = self.url_editar_enunciado()
        texto = "asasdasdasdds"
        response = self.client.post(url, {'numero': NUMERO_ENUNCIADO, 'texto': texto})

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        url_redir = enunciados_url_parser.url_enunciado(self.materia_carrera, self.enunciado)
        self.assertEquals(response.url, url_redir)
        self.enunciado.refresh_from_db()
        self.assertEquals(self.enunciado.versiones.ultima().texto, texto)

    def test_se_puede_hacer_get_a_editar_enunciado_sin_texto(self):
        numero = NUMERO_ENUNCIADO + 1
        Enunciado.objects.create(conjunto=self.practica, numero=numero)
        url = self.url_editar_enunciado(numero)
        response = self.client.get(url)

        self.assertEquals(response.status_code, HTTPStatus.OK)
