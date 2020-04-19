from django.test import TestCase
from django.urls import reverse
from enunciados.models import Universidad, Materia, Carrera, MateriaCarrera, Practica
from enunciados.utils import conjuntos_url_parser


class UrlConjuntoTests(TestCase):
    def setUp(self):
        universidad = Universidad.objects.create(nombre='uba')
        carrera = Carrera.objects.create(
            nombre='Computación', slug='compu', universidad=universidad)
        materia = Materia.objects.create()
        self.materia_carrera = MateriaCarrera.objects.create(
            nombre='materia', slug='materia', carrera=carrera, materia=materia
        )

    def test_con_practica_no_guardada(self):
        """Debería devolver la URL correspondiente."""
        practica = Practica(
            materia=self.materia_carrera.materia,
            anio=2018, cuatrimestre=1, numero=1
        )
        url = conjuntos_url_parser.url_conjunto(self.materia_carrera, practica)
        url_esperada = reverse(
            'materia:practicas:practica:practica', kwargs={
                'materia_carrera': self.materia_carrera,
                'anio': 2018,
                'cuatrimestre': 1,
                'numero_practica': 1,
            }
        )
        self.assertEqual(url_esperada, url)
