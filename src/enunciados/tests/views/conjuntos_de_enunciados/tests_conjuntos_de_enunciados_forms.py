from django.test import TestCase

from enunciados.models import (
    Universidad, Carrera, MateriaCarrera, Materia, Parcial, Practica
)
from enunciados.views.conjuntos_de_enunciados.conjuntos_de_enunciados_forms import (
    ParcialForm, PracticaForm
)


def crear_materia_carrera():
    universidad = Universidad.objects.create()
    carrera = Carrera.objects.create(
        universidad=universidad, nombre='carrera', slug='carrera')
    materia = Materia.objects.create()
    return MateriaCarrera.objects.create(
        materia=materia, carrera=carrera, nombre='materia', slug='materia'
    )


class PracticaFormTests(TestCase):
    def test_guardar_practica_ya_existente(self):
        """Debería no guardarla."""
        materia_carrera = crear_materia_carrera()
        anio = 2018
        cuatrimestre = 1
        numero = 1
        practica_existente = Practica.objects.create(
            materia=materia_carrera.materia, anio=2018,
            cuatrimestre=cuatrimestre, numero=numero
        )
        form = PracticaForm(
            materia_carrera,
            {
                'anio': anio,
                'cuatrimestre': cuatrimestre,
                'numero': numero,
            }
        )

        with self.assertRaises(ValueError):
            form.save()


class ParcialFormTest(TestCase):
    def test_guardar_parcial_ya_existente(self):
        """Debería no guardarlo."""
        materia_carrera = crear_materia_carrera()
        anio = 2018
        cuatrimestre = 1
        numero = 1
        parcial_existente = Parcial.objects.create(
            materia=materia_carrera.materia, anio=2018,
            cuatrimestre=cuatrimestre, numero=numero
        )
        form = ParcialForm(
            materia_carrera,
            {
                'anio': anio,
                'cuatrimestre': cuatrimestre,
                'numero': numero,
            }
        )

        with self.assertRaises(ValueError):
            form.save()
