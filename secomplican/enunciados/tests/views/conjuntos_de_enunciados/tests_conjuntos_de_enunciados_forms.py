from django.test import TestCase

from enunciados.views.conjuntos_de_enunciados.conjuntos_de_enunciados_forms import PracticaForm
from enunciados.models import Materia, Practica


class PracticaFormTests(TestCase):
    def test_guardar_practica_ya_existente(self):
        """Debería no guardarla."""
        materia = Materia.objects.create()
        anio = 2018
        cuatrimestre = 1
        numero = 1
        practica_existente = Practica.objects.create(
            materia=materia, anio=2018,
            cuatrimestre=cuatrimestre, numero=numero
        )
        form = PracticaForm(
            materia,
            {
                'anio': anio,
                'cuatrimestre': cuatrimestre,
                'numero': numero,
            }
        )

        with self.assertRaises(ValueError):
            form.save()
