from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from enunciados.models import (
    Universidad, Carrera, Materia, MateriaCarrera, Practica, Enunciado, Solucion
)
from enunciados.views.soluciones.votar import PUNTOS_USUARIO_POR_VOTO


class VotarSolucionTests(TestCase):
    def setUp(self):
        universidad = Universidad.objects.create(nombre='uba')
        carrera = Carrera.objects.create(
            nombre='Computación', slug='compu', universidad=universidad)
        materia = Materia.objects.create()
        materia_carrera = MateriaCarrera.objects.create(
            nombre='materia', slug='materia', carrera=carrera, materia=materia
        )
        practica = Practica.objects.create(
            materia=materia, anio=2018, cuatrimestre=1, numero=1
        )
        enunciado = Enunciado.objects.create(conjunto=practica, numero=1)
        self.creador = User.objects.create_user(username='user', password='')
        self.solucion = Solucion.objects.create(
            enunciado_padre=enunciado, creador=self.creador)

    def url_de_namespace(self, namespace):
        return reverse(namespace, kwargs={'id_solucion': self.solucion.id})

    def url_votar_arriba(self):
        return self.url_de_namespace('solucion:votar_arriba')

    def url_sacar_voto(self):
        return self.url_de_namespace('solucion:sacar_voto')

    def url_votar_abajo(self):
        return self.url_de_namespace('solucion:votar_abajo')

    def cliente_logueado(self):
        client = Client()
        client.login(username=self.creador.username, password='')
        return client

    def assert_puntos_de_solucion_son(self, puntos):
        self.solucion.refresh_from_db()
        self.assertEquals(self.solucion.puntos, puntos)
        self.creador.refresh_from_db()
        self.assertEquals(
            self.creador.informacionusuario.puntos, puntos * PUNTOS_USUARIO_POR_VOTO)

    def test_votar_arriba_logueado_deberia_sumar_un_voto(self):
        client = self.cliente_logueado()

        response = client.post(self.url_votar_arriba())
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(1)

    def test_votar_arriba_deslogueado_no_deberia_sumar_votos(self):
        client = Client()

        response = client.post(self.url_votar_arriba())
        self.assertEquals(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assert_puntos_de_solucion_son(0)

    def test_votar_arriba_mas_de_una_vez_no_deberia_sumar_mas_de_un_voto(self):
        client = self.cliente_logueado()

        url = self.url_votar_arriba()
        client.post(url)
        response = client.post(url)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(1)

    def test_votar_arriba_por_dos_usuarios_deberia_sumar_un_voto_por_cada_uno(self):
        client = self.cliente_logueado()

        url = self.url_votar_arriba()
        client.post(url)

        segundo_usuario = User.objects.create_user(username='user2', password='pass2')
        client.login(username='user2', password='pass2')
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(2)

    def test_solo_se_puede_votar_arriba_en_una_solucion_valido(self):
        client = self.cliente_logueado()

        url = reverse('solucion:votar_arriba', kwargs={'id_solucion': self.solucion.id + 1})
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)
        self.assert_puntos_de_solucion_son(0)

    def test_solo_se_puede_votar_arriba_con_un_post(self):
        client = self.cliente_logueado()

        url = self.url_votar_arriba()
        response = client.get(url)

        self.assertEquals(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assert_puntos_de_solucion_son(0)

    def test_no_se_puede_sacar_voto_sin_cliente_logueado(self):
        client = Client()

        url = self.url_sacar_voto()
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assert_puntos_de_solucion_son(0)

    def test_no_se_puede_sacar_voto_sin_haber_votado(self):
        client = self.cliente_logueado()

        url = self.url_sacar_voto()
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(0)

    def test_sacar_voto_despues_de_votar_arriba(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)
        url_sacar = self.url_sacar_voto()
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(0)

    def test_no_se_puede_sacar_voto_de_otro_usuario(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        segundo_usuario = User.objects.create_user(username='user2', password='pass2')
        client.login(username='user2', password='pass2')
        url_sacar = self.url_sacar_voto()
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(1)

    def test_no_se_puede_sacar_voto_dos_veces_seguidas(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url_sacar = self.url_sacar_voto()
        client.post(url_sacar)
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(0)

    def test_solo_se_puede_sacar_voto_con_un_post(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url_sacar = self.url_sacar_voto()
        response = client.get(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assert_puntos_de_solucion_son(1)

    def test_solo_se_puede_sacar_voto_en_una_solucion_valido(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url_sacar = reverse('solucion:sacar_voto', kwargs={'id_solucion': self.solucion.id + 1})
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)
        self.assert_puntos_de_solucion_son(1)

    def test_no_se_puede_bajar_de_cero(self):
        client = self.cliente_logueado()

        url_abajo = self.url_votar_abajo()
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(0)

    def test_no_se_puede_votar_abajo_deslogueado(self):
        client = Client()

        url_abajo = self.url_votar_abajo()
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assert_puntos_de_solucion_son(0)

    def test_votar_abajo_mas_de_una_vez_no_deberia_restar_mas_de_un_voto(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)
        segundo_usuario = User.objects.create_user(username='user2', password='pass2')
        client.login(username='user2', password='pass2')
        client.post(url_arriba)
        tercer_usuario = User.objects.create_user(username='user3', password='pass3')
        client.login(username='user3', password='pass3')
        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(1)

    def test_votar_abajo_por_dos_usuarios_deberia_sacar_un_voto_por_cada_usuario(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        User.objects.create_user(username='user2', password='pass2')
        client.login(username='user2', password='pass2')
        client.post(url_arriba)

        url_abajo = self.url_votar_abajo()
        User.objects.create_user(username='user3', password='pass3')
        client.login(username='user3', password='pass3')
        client.post(url_abajo)

        User.objects.create_user(username='user4', password='pass4')
        client.login(username='user4', password='pass4')
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(0)

    def test_votar_abajo_despues_de_votar_arriba(self):
        """Debería no sacar el positivo porque se iría el puntaje a negativo"""
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url_abajo = self.url_votar_abajo()
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(1)

    def test_votar_arriba_despues_de_votar_abajo(self):
        """Debería poner solo el positivo"""
        client = self.cliente_logueado()

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)

        url_arriba = self.url_votar_arriba()
        response = client.post(url_arriba)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(1)

    def test_votar_arriba_abajo_arriba(self):
        """Debería poner solo el primer positivo"""
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)
        response = client.post(url_arriba)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(1)

    def test_sacar_voto_despues_de_votar_abajo(self):
        client = self.cliente_logueado()

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)

        url_sacar = self.url_sacar_voto()
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(0)

    def test_solo_se_puede_votar_abajo_en_un_solucion_valido(self):
        client = self.cliente_logueado()

        url = reverse('solucion:votar_abajo', kwargs={'id_solucion': self.solucion.id + 1})
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)
        self.assert_puntos_de_solucion_son(0)

    def test_sacar_un_voto_no_saca_votos_de_otros(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        User.objects.create_user(username='user3', password='pass3')
        client.login(username='user3', password='pass3')
        client.post(url_arriba)

        url_sacar = self.url_sacar_voto()
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(1)

    def test_sacar_voto_negativo_deberia_aumentar_puntos(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        User.objects.create_user(username='user3', password='pass3')
        client.login(username='user3', password='pass3')

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)

        url_sacar = self.url_sacar_voto()
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assert_puntos_de_solucion_son(1)





