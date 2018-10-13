import datetime

from django.test import TestCase
from enunciados.models import Carrera, Final, Materia, MateriaCarrera, Parcial, \
    Practica, Universidad
from enunciados.utils.conjuntos_utils import castear_a_subclase


class CastearASubclaseTests(TestCase):
    def setUp(self):
        self.materia = Materia.objects.create()

    def test_con_conjunto_con_practica(self):
        """Debería devolver la Practica correspondiente."""
        practica = Practica.objects.create(
            materia=self.materia, anio=2018, cuatrimestre=1, numero=1)
        self.assertIsInstance(
            castear_a_subclase(practica.conjuntodeenunciados_ptr),
            Practica
        )

    def test_con_conjunto_con_parcial(self):
        """Debería devolver el Parcial correspondiente."""
        parcial = Parcial.objects.create(
            materia=self.materia, anio=2018, cuatrimestre=1, numero=1)
        self.assertIsInstance(
            castear_a_subclase(parcial.conjuntodeenunciados_ptr),
            Parcial
        )

    def test_con_conjunto_con_final(self):
        """Debería devolver el Final correspondiente."""
        final = Final.objects.create(
            materia=self.materia, fecha=datetime.date.today()
        )
        self.assertIsInstance(
            castear_a_subclase(final.conjuntodeenunciados_ptr),
            Final
        )

    def test_con_practica_no_guardada(self):
        """Debería devolver la misma Practica."""
        practica = Practica()
        self.assertEqual(castear_a_subclase(practica), practica)

    def test_con_parcial_no_guardado(self):
        """Debería devolver el mismo Parcial."""
        parcial = Parcial()
        self.assertEqual(castear_a_subclase(parcial), parcial)

    def test_con_final_no_guardado(self):
        """Debería devolver el mismo Final."""
        final = Final()
        self.assertEqual(castear_a_subclase(final), final)
