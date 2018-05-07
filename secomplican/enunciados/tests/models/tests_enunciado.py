from django.test import TestCase
from enunciados.models import Materia, Cuatrimestre, ConjuntoDeEnunciados, Enunciado


def agregar_enunciado(conjunto, numero):
    enunciado = Enunciado(conjunto=conjunto, numero=numero)
    enunciado.save()
    return enunciado


class EnunciadoTests(TestCase):
    def setUp(self):
        materia = Materia(nombre='Materia')
        materia.save()
        cuatrimestre = Cuatrimestre(anio=2018, numero=1)
        cuatrimestre.save()
        self.conjunto = ConjuntoDeEnunciados(materia=materia, cuatrimestre=cuatrimestre)
        self.conjunto.save()

    def test_ordenamiento(self):
        """Deberían estar ordenados por numero ascendiente."""
        agregar_enunciado(self.conjunto, 2)
        agregar_enunciado(self.conjunto, 4)
        agregar_enunciado(self.conjunto, 1)
        agregar_enunciado(self.conjunto, 3)

        enunciados = Enunciado.objects.all()
        for index, enunciado in enumerate(enunciados):
            self.assertEquals(enunciado.numero, index + 1)
