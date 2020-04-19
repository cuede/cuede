from django.test import TestCase

from enunciados.models import Materia, Practica, Enunciado


def agregar_enunciado(conjunto, numero):
    return Enunciado.objects.create(conjunto=conjunto, numero=numero)


class EnunciadoTests(TestCase):
    def test_ordenamiento(self):
        """Deberían estar ordenados por numero ascendiente."""
        practica = Practica.objects.create(
            materia=Materia.objects.create(), anio=2018,
            cuatrimestre=1, numero=1)
        agregar_enunciado(practica, 2)
        agregar_enunciado(practica, 4)
        agregar_enunciado(practica, 1)
        agregar_enunciado(practica, 3)

        enunciados = Enunciado.objects.all()
        for index, enunciado in enumerate(enunciados):
            self.assertEquals(enunciado.numero, index + 1)
