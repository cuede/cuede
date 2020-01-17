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
        self.user = get_user_model().objects.create_user(username='user', password='')
        self.enunciado = self.crear_enunciado(NUMERO_ENUNCIADO)
        self.version_texto = self.enunciado.versiones.ultima()

    def crear_enunciado(self, numero):
        enunciado = Enunciado.objects.create(conjunto=self.practica, numero=numero)
        VersionTexto.versiones.create(texto='hola', posteo=enunciado, autor=self.user)
        return enunciado

    def url_editar_enunciado(self, numero=NUMERO_ENUNCIADO):
        return reverse('materia:practicas:practica:enunciados:editar_enunciado', kwargs={
            'materia_carrera': self.materia_carrera,
            'anio': 2018,
            'cuatrimestre': 1,
            'numero_practica': 1,
            'numero': numero,
        })

    def loguear_usuario(self):
        self.client.login(username='user', password='')
        return self.user

    def assert_redirecciona_a_login(self, response, next_url):
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        url_redir = reverse('login') + '?next=' + next_url
        self.assertEquals(response.url, url_redir)

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
        self.loguear_usuario()

        url = self.url_editar_enunciado()
        response = self.client.post(url, {'numero': NUMERO_ENUNCIADO, 'texto': 'asdsadsad'})

        self.user.refresh_from_db()
        self.assertEquals(self.user.informacionusuario.puntos, PUNTOS_USUARIO_EDITAR_ENUNCIADO)

    def test_editar_enunciado_en_un_get_no_suma_puntos_al_usuario(self):
        self.loguear_usuario()

        url = self.url_editar_enunciado()
        response = self.client.get(url)

        self.user.refresh_from_db()
        self.assertEquals(self.user.informacionusuario.puntos, 0)

    def test_editar_enunciado_invalido_no_suma_puntos_al_usuario(self):
        self.loguear_usuario()

        url = self.url_editar_enunciado()
        response = self.client.post(url, {'numero': NUMERO_ENUNCIADO, 'texto': ''})

        self.user.refresh_from_db()
        self.assertEquals(self.user.informacionusuario.puntos, 0)

    def test_editar_enunciado_sin_cambiar_texto_no_suma_puntos_al_usuario(self):
        self.loguear_usuario()

        url = self.url_editar_enunciado()
        response = self.client.post(url, {
            'numero': NUMERO_ENUNCIADO, 'texto': self.version_texto.texto
        })

        self.user.refresh_from_db()
        self.assertEquals(self.user.informacionusuario.puntos, 0)

    def test_cambiar_solo_numero_de_enunciado_no_suma_puntos(self):
        self.loguear_usuario()

        url = self.url_editar_enunciado()
        response = self.client.post(url, {
            'numero': NUMERO_ENUNCIADO + 1, 'texto': self.version_texto.texto
        })

        self.user.refresh_from_db()
        self.assertEquals(self.user.informacionusuario.puntos, 0)

    def test_editar_dos_enunciados_diferentes_suma_una_vez_por_cada_uno(self):
        self.loguear_usuario()

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

        self.user.refresh_from_db()
        self.assertEquals(
            self.user.informacionusuario.puntos, PUNTOS_USUARIO_EDITAR_ENUNCIADO * 2)

    def test_editar_mismo_enunciado_dos_veces_no_da_puntos_mas_de_una_vez(self):
        self.loguear_usuario()

        url = self.url_editar_enunciado()
        self.client.post(url, {
            'numero': NUMERO_ENUNCIADO, 'texto': self.version_texto.texto + 'ASDSADASD'
        })
        self.client.post(url, {
            'numero': NUMERO_ENUNCIADO, 'texto': self.version_texto.texto + 'sdsds'
        })

        self.user.refresh_from_db()
        self.assertEquals(
            self.user.informacionusuario.puntos, PUNTOS_USUARIO_EDITAR_ENUNCIADO)

