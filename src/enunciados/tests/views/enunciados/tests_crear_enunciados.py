from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from enunciados.models import Universidad, Carrera, Materia, MateriaCarrera, Practica, Enunciado

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

    def post_crear_enunciado(self, url, texto=TEXTO_ENUNCIADO):
        return self.client.post(url, {'numero': NUMERO_ENUNCIADO, 'texto': texto})

    def assert_response_redirecciona_a_enunciado(self, response):
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        url_redir = self.url_enunciado_creado()
        self.assertEquals(response.url, url_redir)

    def assert_enunciado_fue_creado(self):
        self.assertEquals(Enunciado.objects.count(), 1)
        enunciado = Enunciado.objects.all().first()
        self.assertEquals(enunciado.numero, NUMERO_ENUNCIADO)
        return enunciado

    def test_se_puede_crear_un_enunciado_con_texto(self):
        response = self.post_crear_enunciado(self.url_crear_enunciado())

        self.assert_response_redirecciona_a_enunciado(response)
        enunciado = self.assert_enunciado_fue_creado()
        self.assertEquals(enunciado.versiones.ultima().texto, TEXTO_ENUNCIADO)

    def test_no_se_puede_crear_un_enunciado_sin_texto_cuando_no_hay_archivo_de_enunciados(self):
        url_crear_enunciado = self.url_crear_enunciado()
        response = self.post_crear_enunciado(url_crear_enunciado, texto='')

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(Enunciado.objects.count(), 0)

    def test_se_puede_crear_un_enunciado_sin_texto_cuando_hay_archivo_de_enunciados(self):
        self.practica.archivo = 'hola'
        self.practica.save()
        texto = ''

        url_crear_enunciado = self.url_crear_enunciado()
        response = self.post_crear_enunciado(url_crear_enunciado, texto=texto)

        self.assert_response_redirecciona_a_enunciado(response)
        enunciado = self.assert_enunciado_fue_creado()
        self.assertEquals(enunciado.versiones.count(), 0)

    def test_se_puede_crear_un_enunciado_con_texto_cuando_hay_archivo_de_enunciados(self):
        self.practica.archivo = 'hola'
        self.practica.save()

        url_crear_enunciado = self.url_crear_enunciado()
        response = self.post_crear_enunciado(url_crear_enunciado)

        self.assert_response_redirecciona_a_enunciado(response)
        enunciado = self.assert_enunciado_fue_creado()
        self.assertEquals(enunciado.versiones.ultima().texto, TEXTO_ENUNCIADO)
