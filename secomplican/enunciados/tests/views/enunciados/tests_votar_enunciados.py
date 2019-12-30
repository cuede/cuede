from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from enunciados.models import Universidad, Carrera, Materia, MateriaCarrera, Practica, Enunciado


def crear_usuario(username, password):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    return user


class VotarEnunciadoTests(TestCase):
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
        Enunciado.objects.create(conjunto=practica, numero=1)

    def url_de_namespace(self, namespace):
        return reverse(namespace, kwargs={
                'materia_carrera': self.materia_carrera,
                'anio': 2018,
                'cuatrimestre': 1,
                'numero_practica': 1,
                'numero': 1,
            }
        )

    def url_votar_arriba(self):
        return self.url_de_namespace(
            'materia:practicas:practica:enunciados:votar_arriba'
        )

    def url_sacar_voto(self):
        return self.url_de_namespace(
            'materia:practicas:practica:enunciados:sacar_voto'
        )

    def url_votar_abajo(self):
        return self.url_de_namespace(
            'materia:practicas:practica:enunciados:votar_abajo'
        )

    def cliente_logueado(self):
        user = crear_usuario('user', 'pass')
        client = Client()
        client.login(username='user', password='pass')
        return client

    def test_votar_arriba_logueado_deberia_sumar_un_voto(self):
        client = self.cliente_logueado()

        response = client.post(self.url_votar_arriba())
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 1)

    def test_votar_arriba_deslogueado_no_deberia_sumar_votos(self):
        client = Client()

        response = client.post(self.url_votar_arriba())
        self.assertEquals(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEquals(Enunciado.objects.all()[0].votos, 0)

    def test_votar_arriba_mas_de_una_vez_no_deberia_sumar_mas_de_un_voto(self):
        client = self.cliente_logueado()

        url = self.url_votar_arriba()
        client.post(url)
        response = client.post(url)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 1)

    def test_votar_arriba_por_dos_usuarios_deberia_sumar_un_voto_por_cada_uno(self):
        client = self.cliente_logueado()

        url = self.url_votar_arriba()
        client.post(url)

        segundo_usuario = crear_usuario('user2', 'pass2')
        client.login(username='user2', password='pass2')
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 2)

    def test_solo_se_puede_votar_arriba_en_un_enunciado_valido(self):
        client = self.cliente_logueado()

        url = reverse(
            'materia:practicas:practica:enunciados:votar_arriba',
            kwargs={
                'materia_carrera': self.materia_carrera,
                'anio': 2018,
                'cuatrimestre': 1,
                'numero_practica': 1,
                'numero': 2,
            }
        )
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEquals(Enunciado.objects.all()[0].votos, 0)

    def test_solo_se_puede_votar_arriba_con_un_post(self):
        client = self.cliente_logueado()

        url = self.url_votar_arriba()
        response = client.get(url)

        self.assertEquals(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEquals(Enunciado.objects.all()[0].votos, 0)

    def test_no_se_puede_sacar_voto_sin_cliente_logueado(self):
        client = Client()

        url = self.url_sacar_voto()
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEquals(Enunciado.objects.all()[0].votos, 0)

    def test_no_se_puede_sacar_voto_sin_haber_votado(self):
        client = self.cliente_logueado()

        url = self.url_sacar_voto()
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 0)

    def test_sacar_voto_despues_de_votar_arriba(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)
        url_sacar = self.url_sacar_voto()
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 0)

    def test_no_se_puede_sacar_voto_de_otro_usuario(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        segundo_usuario = crear_usuario('user2', 'pass2')
        client.login(username='user2', password='pass2')
        url_sacar = self.url_sacar_voto()
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 1)

    def test_no_se_puede_sacar_voto_dos_veces_seguidas(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url_sacar = self.url_sacar_voto()
        client.post(url_sacar)
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 0)

    def test_solo_se_puede_sacar_voto_con_un_post(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url_sacar = self.url_sacar_voto()
        response = client.get(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEquals(Enunciado.objects.all()[0].votos, 1)

    def test_solo_se_puede_sacar_voto_en_un_enunciado_valido(self):
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url = reverse(
            'materia:practicas:practica:enunciados:sacar_voto',
            kwargs={
                'materia_carrera': self.materia_carrera,
                'anio': 2018,
                'cuatrimestre': 1,
                'numero_practica': 1,
                'numero': 2,
            }
        )
        response = client.post(url)

        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEquals(Enunciado.objects.all()[0].votos, 1)

    def test_votar_abajo_baja_un_voto_del_enunciado(self):
        client = self.cliente_logueado()

        url_abajo = self.url_votar_abajo()
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, -1)

    def test_no_se_puede_votar_abajo_deslogueado(self):
        client = Client()

        url_abajo = self.url_votar_abajo()
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEquals(Enunciado.objects.all()[0].votos, 0)

    def test_votar_abajo_mas_de_una_vez_no_deberia_restar_mas_de_un_voto(self):
        client = self.cliente_logueado()

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, -1)

    def test_votar_abajo_por_dos_usuarios_deberia_sacar_un_voto_por_cada_usuario(self):
        client = self.cliente_logueado()

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)

        segundo_usuario = crear_usuario('user2', 'pass2')
        client.login(username='user2', password='pass2')
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, -2)

    def test_votar_abajo_despues_de_votar_arriba(self):
        """Debería sacar el positivo y poner el negativo"""
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url_abajo = self.url_votar_abajo()
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, -1)

    def test_votar_arriba_despues_de_votar_abajo(self):
        """Debería sacar el negativo y poner el positivo"""
        client = self.cliente_logueado()

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)

        url_arriba = self.url_votar_arriba()
        response = client.post(url_arriba)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 1)

    def test_votar_abajo_arriba_abajo(self):
        """Debería sacar el negativo y poner el positivo"""
        client = self.cliente_logueado()

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)
        response = client.post(url_abajo)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, -1)

    def test_votar_arriba_abajo_arriba(self):
        """Debería sacar el negativo y poner el positivo"""
        client = self.cliente_logueado()

        url_arriba = self.url_votar_arriba()
        client.post(url_arriba)

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)
        response = client.post(url_arriba)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 1)

    def test_sacar_voto_despues_de_votar_abajo(self):
        client = self.cliente_logueado()

        url_abajo = self.url_votar_abajo()
        client.post(url_abajo)

        url_sacar = self.url_sacar_voto()
        response = client.post(url_sacar)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.all()[0].votos, 0)