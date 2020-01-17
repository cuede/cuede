from unittest import skip
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from enunciados.models import (
    Universidad, Carrera, Materia, MateriaCarrera, Practica, Enunciado, VersionTexto
)
from enunciados.views.enunciados.editar import PUNTOS_USUARIO_EDITAR_ENUNCIADO


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
        self.usuario_creador = get_user_model().objects.create_user(
            username='user', password='')
        self.usuario_editor = get_user_model().objects.create_user(
            username='editor', password='')
        self.enunciado = self.crear_enunciado(NUMERO_ENUNCIADO)
        self.version_texto = self.enunciado.versiones.ultima()

    def crear_enunciado(self, numero):
        enunciado = Enunciado.objects.create(conjunto=self.practica, numero=numero)
        VersionTexto.versiones.create(
            texto='hola', posteo=enunciado, autor=self.usuario_creador)
        return enunciado

    def url_editar_enunciado(self, numero=NUMERO_ENUNCIADO):
        return reverse('materia:practicas:practica:enunciados:editar_enunciado', kwargs={
            'materia_carrera': self.materia_carrera,
            'anio': 2018,
            'cuatrimestre': 1,
            'numero_practica': 1,
            'numero': numero,
        })

    def loguear_usuario_editor(self):
        self.client.login(username='editor', password='')

    def assert_redirecciona_a_login(self, response, next_url):
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        url_redir = reverse('login') + '?next=' + next_url
        self.assertEquals(response.url, url_redir)

    def assert_puntos_de_usuario_editor_son(self, puntos):
        self.usuario_editor.refresh_from_db()
        self.assertEquals(
            self.usuario_editor.informacionusuario.puntos, puntos)

    def test_no_se_puede_editar_un_enunciado_sin_loguearse(self):
        url = self.url_editar_enunciado()
        response = self.client.post(url)

        self.assert_redirecciona_a_login(response, url)
        self.enunciado.refresh_from_db()
        self.assertEquals(self.enunciado.versiones.ultima(), self.version_texto)

    def test_no_se_puede_hacer_get_a_editar_un_enunciado_sin_loguearse(self):
        url = self.url_editar_enunciado()
        response = self.client.get(url)

        self.assert_redirecciona_a_login(response, url)
        self.enunciado.refresh_from_db()
        self.assertEquals(self.enunciado.versiones.ultima(), self.version_texto)

    def test_editar_enunciado_suma_puntos_al_usuario(self):
        self.loguear_usuario_editor()

        url = self.url_editar_enunciado()
        response = self.client.post(url, {'numero': NUMERO_ENUNCIADO, 'texto': 'asdsadsad'})

        self.assert_puntos_de_usuario_editor_son(PUNTOS_USUARIO_EDITAR_ENUNCIADO)

    def test_editar_enunciado_en_un_get_no_suma_puntos_al_usuario(self):
        self.loguear_usuario_editor()

        url = self.url_editar_enunciado()
        response = self.client.get(url)

        self.assert_puntos_de_usuario_editor_son(0)

    def test_editar_enunciado_invalido_no_suma_puntos_al_usuario(self):
        self.loguear_usuario_editor()

        url = self.url_editar_enunciado()
        response = self.client.post(url, {'numero': NUMERO_ENUNCIADO, 'texto': ''})

        self.assert_puntos_de_usuario_editor_son(0)

    def test_editar_enunciado_sin_cambiar_texto_no_suma_puntos_al_usuario(self):
        self.loguear_usuario_editor()

        url = self.url_editar_enunciado()
        response = self.client.post(url, {
            'numero': NUMERO_ENUNCIADO, 'texto': self.version_texto.texto
        })

        self.assert_puntos_de_usuario_editor_son(0)

    def test_cambiar_solo_numero_de_enunciado_no_suma_puntos(self):
        self.loguear_usuario_editor()

        url = self.url_editar_enunciado()
        response = self.client.post(url, {
            'numero': NUMERO_ENUNCIADO + 1, 'texto': self.version_texto.texto
        })

        self.assert_puntos_de_usuario_editor_son(0)

    def test_editar_dos_enunciados_diferentes_suma_una_vez_por_cada_uno(self):
        self.loguear_usuario_editor()

        numero_enunciado_2 = NUMERO_ENUNCIADO + 1
        enunciado_2 = self.crear_enunciado(numero_enunciado_2)

        url = self.url_editar_enunciado()
        self.client.post(url, {
            'numero': NUMERO_ENUNCIADO, 'texto': self.version_texto.texto + 'ASDSADASD'
        })
        url2 = self.url_editar_enunciado(numero=numero_enunciado_2)
        self.client.post(url2, {
            'numero': numero_enunciado_2, 'texto': self.version_texto.texto + 'ASDSADASD'
        })

        self.assert_puntos_de_usuario_editor_son(PUNTOS_USUARIO_EDITAR_ENUNCIADO * 2)

    def test_editar_mismo_enunciado_dos_veces_no_da_puntos_mas_de_una_vez(self):
        self.loguear_usuario_editor()

        url = self.url_editar_enunciado()
        self.client.post(url, {
            'numero': NUMERO_ENUNCIADO, 'texto': self.version_texto.texto + 'ASDSADASD'
        })
        self.client.post(url, {
            'numero': NUMERO_ENUNCIADO, 'texto': self.version_texto.texto + 'sdsds'
        })

        self.assert_puntos_de_usuario_editor_son(PUNTOS_USUARIO_EDITAR_ENUNCIADO)

    def test_dos_usuarios_editando_el_mismo_enunciado_cada_uno_gana_puntos(self):
        self.loguear_usuario_editor()

        url = self.url_editar_enunciado()
        self.client.post(url, {
            'numero': NUMERO_ENUNCIADO, 'texto': self.version_texto.texto + 'ASDSADASD'
        })

        nuevo_usuario = get_user_model().objects.create_user(
            username='nuevo', password='')
        self.client.login(username='nuevo', password='')
        self.client.post(url, {
            'numero': NUMERO_ENUNCIADO, 'texto': self.version_texto.texto + 'asdsdsdsd'
        })

        self.assert_puntos_de_usuario_editor_son(PUNTOS_USUARIO_EDITAR_ENUNCIADO)
        nuevo_usuario.refresh_from_db()
        self.assertEquals(
            nuevo_usuario.informacionusuario.puntos, PUNTOS_USUARIO_EDITAR_ENUNCIADO)
