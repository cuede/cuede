from django.test import TestCase
from django.urls import reverse

from enunciados.utils import cuatrimestres_url_parser
from enunciados.models import Materia, Practica, Parcial, Enunciado, Final


def agregar_enunciado(conjunto, numero):
    enunciado = Enunciado(conjunto=conjunto, numero=numero)
    enunciado.save()
    return enunciado


class EnunciadoTests(TestCase):
    def setUp(self):
        self.materia = Materia(nombre='Materia')
        self.materia.save()
        self.cuatrimestre = 1

    def crear_practica(self):
        practica = Practica(materia=self.materia, anio=2018, cuatrimestre=self.cuatrimestre, numero=1)
        practica.save()
        return practica

    def crear_parcial(self, recuperatorio=False):
        parcial = Parcial(materia=self.materia, anio=2018, cuatrimestre=self.cuatrimestre, numero=1, recuperatorio=recuperatorio)
        parcial.save()
        return parcial

    def crear_final(self):
        import datetime
        final = Final(materia=self.materia, fecha=datetime.date.today())
        final.save()
        return final

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
        practica = self.crear_practica()
        enunciado = Enunciado(conjunto=practica, numero=1)
        enunciado.save()

        url_esperada = reverse('enunciado_practica', kwargs={
            'materia': practica.materia.nombre,
            'anio': practica.anio,
            'cuatrimestre': cuatrimestres_url_parser.numero_a_url(practica.cuatrimestre),
            'numero_practica': practica.numero,
            'numero': enunciado.numero,
        })

        self.assertEquals(enunciado.get_absolute_url(), url_esperada)

    def test_get_absolute_url_con_parcial(self):
        """Debería devolver la URL correspondiente."""
        parcial = self.crear_parcial()
        enunciado = Enunciado(conjunto=parcial, numero=1)
        enunciado.save()

        url_esperada = reverse('enunciado_parcial', kwargs={
            'materia': parcial.materia.nombre,
            'anio': parcial.anio,
            'cuatrimestre': cuatrimestres_url_parser.numero_a_url(parcial.cuatrimestre),
            'numero_parcial': parcial.numero,
            'numero': enunciado.numero,
        })

        self.assertEquals(enunciado.get_absolute_url(), url_esperada)

    def test_get_absolute_url_con_recuperatorio(self):
        """Debería devolver la URL correspondiente."""
        recuperatorio = self.crear_parcial(recuperatorio=True)
        enunciado = Enunciado(conjunto=recuperatorio, numero=1)
        enunciado.save()

        url_esperada = reverse('enunciado_recuperatorio', kwargs={
            'materia': recuperatorio.materia.nombre,
            'anio': recuperatorio.anio,
            'cuatrimestre': cuatrimestres_url_parser.numero_a_url(recuperatorio.cuatrimestre),
            'numero_parcial': recuperatorio.numero,
            'numero': enunciado.numero,
        })

        self.assertEquals(enunciado.get_absolute_url(), url_esperada)

    def test_get_absolute_url_con_final(self):
        """Debería devolver la URL correspondiente."""
        final = self.crear_final()
        enunciado = Enunciado(conjunto=final, numero=1)
        enunciado.save()

        url_esperada = reverse('enunciado_final', kwargs={
            'materia': final.materia.nombre,
            'anio': final.fecha.year,
            'mes': final.fecha.month,
            'dia': final.fecha.day,
            'numero': enunciado.numero,
        })

        self.assertEquals(enunciado.get_absolute_url(), url_esperada)
