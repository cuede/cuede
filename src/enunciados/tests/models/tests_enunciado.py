from django.core.exceptions import ValidationError
from django.test import TestCase

from enunciados.models import Materia, Practica, Enunciado


class EnunciadoTests(TestCase):

    def setUp(self) -> None:
        self.conjunto = Practica.objects.create(
            materia=Materia.objects.create(), anio=2018,
            cuatrimestre=1, numero=1)

    def test_no_se_puede_crear_un_enunciado_con_numero_negativo(self):
        enunciado = self.enunciado_con_numero(-1)

        with self.assertRaises(Exception):
            enunciado.save()

    def test_no_se_puede_crear_un_enunciado_con_numero_cero(self):
        enunciado = self.enunciado_con_numero(0)

        with self.assertRaises(Exception):
            enunciado.save()

    def test_se_puede_crear_un_enunciado_con_numero_positivo(self):
        self.enunciado_con_numero(1).save()

    def test_limpiar_enunciado_con_numero_negativo_tira_error(self):
        enunciado = self.enunciado_con_numero(0)

        with self.assertRaises(ValidationError):
            enunciado.full_clean()

    def test_limpiar_enunciado_con_numero_cero_tira_error(self):
        enunciado = self.enunciado_con_numero(0)

        with self.assertRaises(ValidationError):
            enunciado.full_clean()

    def test_se_puede_limpiar_enunciado_con_numero_positivo(self):
        self.enunciado_con_numero(1).full_clean()

    def test_ordenamiento(self):
        """Deberían estar ordenados por numero ascendiente."""
        self.agregar_enunciado(2)
        self.agregar_enunciado(4)
        self.agregar_enunciado(1)
        self.agregar_enunciado(3)

        enunciados = Enunciado.objects.all()
        for index, enunciado in enumerate(enunciados):
            self.assertEquals(enunciado.numero, index + 1)

    def agregar_enunciado(self, numero):
        self.enunciado_con_numero(numero).save()

    def enunciado_con_numero(self, numero):
        return Enunciado(conjunto=self.conjunto, numero=numero)
