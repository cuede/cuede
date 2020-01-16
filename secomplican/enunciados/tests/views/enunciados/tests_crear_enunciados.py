from unittest import skip
from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth import get_user_model

from enunciados.models import Universidad, Carrera, Materia, MateriaCarrera, Practica, Enunciado
from enunciados.views.enunciados.crear import PUNTOS_USUARIO_POR_CREAR_ENUNCIADO
from enunciados.utils import enunciados_url_parser


TEXTO_ENUNCIADO = 'asdsadsadsad'
NUMERO_ENUNCIADO = 1

class CrearEnunciadoTests(TestCase):
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

    def loguear_usuario(self):
        user = get_user_model().objects.create_user(username='user', password='')
        self.client.login(username='user', password='')
        return user

    def url_crear_enunciado(self):
        return reverse('materia:practicas:practica:enunciados:nuevo_enunciado', kwargs={
            'materia_carrera': self.materia_carrera,
            'anio': 2018,
            'cuatrimestre': 1,
            'numero_practica': 1,
        })

    def url_enunciado_creado(self):
        return reverse('materia:practicas:practica:enunciados:ver_enunciado', kwargs={
            'materia_carrera': self.materia_carrera,
            'anio': 2018,
            'cuatrimestre': 1,
            'numero_practica': 1,
            'numero': NUMERO_ENUNCIADO,
        })

    def post_crear_enunciado(self, url, numero=NUMERO_ENUNCIADO):
        return self.client.post(url, {'numero': numero, 'texto': TEXTO_ENUNCIADO})

    def assert_enunciado_fue_creado(self):
        self.assertEquals(Enunciado.objects.count(), 1)
        enunciado = Enunciado.objects.all().first()
        self.assertEquals(enunciado.numero, NUMERO_ENUNCIADO)
        self.assertEquals(enunciado.versiones.ultima().texto, TEXTO_ENUNCIADO)

    def assert_redirecciona_a_login(self, response, url):
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        url_redir = reverse('login') + '?next=' + url
        self.assertEquals(response.url, url_redir)

    def test_get_no_estando_logueado_deberia_redirigir(self):
        url = self.url_crear_enunciado()
        response = self.client.get(url)

        self.assert_redirecciona_a_login(response, url)

    def test_se_puede_crear_un_enunciado_estando_logueado(self):
        self.loguear_usuario()

        response = self.post_crear_enunciado(self.url_crear_enunciado())

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        url_redir = self.url_enunciado_creado()
        self.assertEquals(response.url, url_redir)
        self.assert_enunciado_fue_creado()

    def test_no_se_puede_crear_un_enunciado_deslogueado(self):
        url = self.url_crear_enunciado()
        response = self.post_crear_enunciado(url)

        self.assert_redirecciona_a_login(response, url)
        self.assertEquals(Enunciado.objects.count(), 0)

    def test_crear_enunciado_deberia_sumar_puntos_al_usuario(self):
        user = self.loguear_usuario()

        self.post_crear_enunciado(self.url_crear_enunciado())

        user.refresh_from_db()
        self.assertEquals(user.informacionusuario.puntos, PUNTOS_USUARIO_POR_CREAR_ENUNCIADO)

    def test_crear_dos_enunciados_deberia_sumar_puntos_al_usuario_por_cada_uno(self):
        user = self.loguear_usuario()

        self.post_crear_enunciado(self.url_crear_enunciado(), numero=1)
        self.post_crear_enunciado(self.url_crear_enunciado(), numero=2)

        user.refresh_from_db()
        self.assertEquals(
            user.informacionusuario.puntos,
            PUNTOS_USUARIO_POR_CREAR_ENUNCIADO * 2
        )

    @skip(
        'Por alguna razón tratar de hacer render en tests hace que te tire un error de' \
        'staticfiles.'
    )
    def test_get_no_deberia_sumar_puntos(self):
        user = self.loguear_usuario()

        response = self.client.get(self.url_crear_enunciado())

        user.refresh_from_db()
        self.assertEquals(user.informacionusuario.puntos, 0)