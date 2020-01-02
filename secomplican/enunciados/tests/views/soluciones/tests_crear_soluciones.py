from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from enunciados.models import (
    Universidad, Carrera, Materia, MateriaCarrera, Practica, Enunciado, Solucion
)


class CrearSolucionTests(TestCase):
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
        self.enunciado = Enunciado.objects.create(conjunto=practica, numero=1)
        self.creador = User.objects.create_user(username='user', password='')

    def cliente_logueado(self):
        client = Client()
        client.login(username=self.creador.username, password='')
        return client

    def url_crear(self):
        return reverse('materia:practicas:practica:enunciados:crear_solucion', kwargs={
            'materia_carrera': self.materia_carrera,
            'anio': 2018,
            'cuatrimestre': 1,
            'numero_practica': 1,
            'numero': 1,
        })

    def test_crear_solucion_con_usuario_logueado_deberia_crearla(self):
        client = self.cliente_logueado()

        url = self.url_crear()
        response = client.post(url, {'texto': 'asasdsadsa'})

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        url_redir = reverse('materia:practicas:practica:enunciados:ver_enunciado', kwargs={
            'materia_carrera': self.materia_carrera,
            'anio': 2018,
            'cuatrimestre': 1,
            'numero_practica': 1,
            'numero': 1,
        })
        self.assertEquals(response.url, url_redir)
        self.assertEquals(Solucion.objects.all().count(), 1)
        creada = Solucion.objects.all().first()
        self.assertEquals(creada.enunciado_padre, self.enunciado)
        self.assertEquals(creada.creador, self.creador)

    def test_crear_solucion_sin_usuario_logueado_deberia_redireccionar_a_login(self):
        url = self.url_crear()

        response = self.client.post(url, {'texto': 'asdaasdasd'})
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        url_redir = reverse('login') + '?next=' + url
        self.assertEquals(response.url, url_redir)
        self.assertEquals(Solucion.objects.all().count(), 0)



