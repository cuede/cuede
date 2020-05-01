from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from enunciados.models import (
    Universidad, Carrera, Materia, MateriaCarrera, Practica, Enunciado, Solucion, VersionTexto,
    get_sentinel_user
)
from enunciados.utils import enunciados_url_parser
from enunciados.views.soluciones.editar import PUNTOS_USUARIO_POR_EDITAR_SOLUCION


class EditarSolucionTests(TestCase):
    def setUp(self):
        universidad = Universidad.objects.create(nombre='uba')
        carrera = Carrera.objects.create(
            nombre='Computación', slug='compu', universidad=universidad)
        materia = Materia.objects.create()
        self.materia_carrera = MateriaCarrera.objects.create(
            nombre='materia', slug='materia', carrera=carrera, materia=materia
        )
        practica = Practica.objects.create(
            materia=materia, anio=2018, cuatrimestre=1, numero=1
        )
        self.creador = get_user_model().objects.create_user(username='user', password='')
        self.enunciado = Enunciado.objects.create(conjunto=practica, numero=1)
        VersionTexto.versiones.create(texto='un texto', posteo=self.enunciado, autor=self.creador)
        self.editor = get_sentinel_user()
        self.solucion = Solucion.objects.create(
            enunciado_padre=self.enunciado, creador=self.creador)
        self.version_texto = VersionTexto.versiones.create(
            texto='asdsad', posteo=self.solucion, autor=self.creador)

    def url_editar_solucion(self, pk_solucion=None):
        if not pk_solucion:
            pk_solucion = self.solucion.pk
        return reverse('materia:practicas:practica:enunciados:editar_solucion', kwargs={
            'materia_carrera': self.materia_carrera,
            'anio': 2018,
            'cuatrimestre': 1,
            'numero_practica': 1,
            'numero': 1,
            'pk_solucion': pk_solucion,
        })

    def url_ver_enunciado(self):
        return enunciados_url_parser.url_enunciado(self.materia_carrera, self.enunciado)

    def assert_puntos_de_editor_son(self, puntos):
        self.editor.refresh_from_db()
        self.assertEquals(self.editor.informacionusuario.puntos, puntos)

    def test_se_puede_editar_solucion_sin_loguearse(self):
        url = self.url_editar_solucion()
        texto = 'un texto muy largo'
        response = self.client.post(url, {'texto': texto})

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        url_redir = self.url_ver_enunciado()
        self.assertEquals(response.url, url_redir)
        self.assertEquals(self.solucion.versiones.ultima().texto, texto)
        self.assertEquals(self.solucion.versiones.ultima().autor, get_sentinel_user())

    def test_editar_solucion_da_puntos_al_usuario(self):
        self.client.login(username=self.editor.username, password='')

        self.client.post(self.url_editar_solucion(), {'texto': 'asdsdasdasd'})

        self.assert_puntos_de_editor_son(PUNTOS_USUARIO_POR_EDITAR_SOLUCION)

    def test_get_no_da_puntos_al_usuario(self):
        self.client.login(username=self.editor.username, password='')

        self.client.get(self.url_editar_solucion())

        self.assert_puntos_de_editor_son(0)

    def test_form_invalida_no_da_puntos_al_usuario(self):
        self.client.login(username=self.editor.username, password='')

        # No se cambia el texto
        self.client.post(self.url_editar_solucion(), {'texto': self.version_texto.texto})

        self.assert_puntos_de_editor_son(0)

    def test_editar_solucion_no_da_puntos_si_creaste_esa_solucion(self):
        self.client.login(username=self.creador.username, password='')

        self.client.post(self.url_editar_solucion(), {'texto': 'testooooasljdlasdkls'})

        self.creador.refresh_from_db()
        self.assertEquals(self.creador.informacionusuario.puntos, 0)

    def test_editar_dos_soluciones_da_puntos_por_cada_una(self):
        self.client.login(username=self.editor.username, password='')

        solucion2 = Solucion.objects.create(
            enunciado_padre=self.enunciado, creador=self.creador)
        version_texto2 = VersionTexto.versiones.create(
            texto='asdsad', posteo=solucion2, autor=self.creador)

        url = self.url_editar_solucion()
        self.client.post(url, {'texto': 'testooooasljdlasdkls'})
        url2 = self.url_editar_solucion(pk_solucion=solucion2.pk)
        self.client.post(url2, {'texto': 'testooooasljdlasdkls'})

        self.assert_puntos_de_editor_son(PUNTOS_USUARIO_POR_EDITAR_SOLUCION * 2)

    def test_editar_solucion_no_da_puntos_si_ya_editaste_esa_solucion(self):
        self.client.login(username=self.editor.username, password='')

        self.client.post(self.url_editar_solucion(), {'texto': 'testooooasljdlasdkls'})
        self.client.post(self.url_editar_solucion(), {'texto': 'otralakjsdlksajdlk'})

        self.assert_puntos_de_editor_son(PUNTOS_USUARIO_POR_EDITAR_SOLUCION)
