from django.test import TestCase
from enunciados.models import Materia, Cuatrimestre, Practica, Enunciado


def agregar_enunciado(conjunto, numero):
    enunciado = Enunciado(conjunto=conjunto, numero=numero)
    enunciado.save()
    return enunciado


class EnunciadoTests(TestCase):
    def setUp(self):
        self.materia = Materia(nombre='Materia')
        self.materia.save()
        self.cuatrimestre = Cuatrimestre(anio=2018, numero=1)
        self.cuatrimestre.save()

    def crear_practica(self):
        practica = Practica(materia=self.materia, cuatrimestre=self.cuatrimestre, numero=1)
        practica.save()
        return practica

    def test_ordenamiento(self):
        """Deberían estar ordenados por numero ascendiente."""
        practica = self.crear_practica()
        agregar_enunciado(practica, 2)
        agregar_enunciado(practica, 4)
        agregar_enunciado(practica, 1)
        agregar_enunciado(practica, 3)

        enunciados = Enunciado.objects.all()
        for index, enunciado in enumerate(enunciados):
            self.assertEquals(enunciado.numero, index + 1)

    def test_get_absolute_url_con_practica(self):
        """Debería devolver la URL correspondiente."""
        from django.urls import reverse

        from enunciados import cuatrimestres_url_parser

        practica = self.crear_practica()
        enunciado = Enunciado(conjunto=practica, numero=1)
        enunciado.save()

        url_esperada = reverse('enunciado_practica', kwargs={
            'materia': practica.materia.nombre,
            'anio': practica.cuatrimestre.anio,
            'cuatrimestre': cuatrimestres_url_parser.numero_a_url(practica.cuatrimestre.numero),
            'conjunto_de_enunciados': practica.numero,
            'numero': enunciado.numero,
        })

        self.assertEquals(enunciado.get_absolute_url(), url_esperada)

