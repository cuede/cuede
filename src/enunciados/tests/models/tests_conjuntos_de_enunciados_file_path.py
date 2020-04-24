from datetime import date
from unittest import TestCase

from enunciados.models import \
    Materia, Practica, Parcial, Final, \
    ConjuntoDeEnunciadosConCuatrimestre, conjunto_de_enunciados_file_path


class ConjuntosDeEnunciadosFilePathTest(TestCase):
    def setUp(self) -> None:
        self.materia = Materia.objects.create()

    def test_file_path_de_pdf_de_practica_usa_la_pk_de_la_materia_el_cuatrimestre_y_el_numero_de_practica(
            self) -> None:
        numero_practica = 2
        cuatrimestre = ConjuntoDeEnunciadosConCuatrimestre.VERANO
        anio = 2020
        practica = Practica(
            materia=self.materia, anio=anio, cuatrimestre=cuatrimestre, numero=numero_practica)
        path = conjunto_de_enunciados_file_path(practica, 'archivo.pdf')

        expected = '{materia}/practicas/{anio}/{cuatrimestre}/{numero}.pdf'.format(
            materia=self.materia.pk, anio=anio, cuatrimestre=cuatrimestre, numero=numero_practica)
        self.assertEquals(expected, path)

    def test_file_path_de_jpg_de_practica_usa_la_pk_de_la_materia_el_cuatrimestre_y_el_numero_de_practica(
            self) -> None:
        numero_practica = 2
        cuatrimestre = ConjuntoDeEnunciadosConCuatrimestre.VERANO
        anio = 2020
        practica = Practica(
            materia=self.materia, anio=anio, cuatrimestre=cuatrimestre, numero=numero_practica)
        path = conjunto_de_enunciados_file_path(practica, 'archivo.jpg')

        expected = '{materia}/practicas/{anio}/{cuatrimestre}/{numero}.jpg'.format(
            materia=self.materia.pk, anio=anio, cuatrimestre=cuatrimestre,
            numero=numero_practica)

    def test_file_path_de_parcial_no_recuperatorio(self):
        numero_parcial = 4
        cuatrimestre = ConjuntoDeEnunciadosConCuatrimestre.PRIMERO
        anio = 2012
        parcial = Parcial(
            materia=self.materia, anio=anio, cuatrimestre=cuatrimestre, numero=numero_parcial,
            recuperatorio=False)
        path = conjunto_de_enunciados_file_path(parcial, 'archivo.jpeg')

        expected = '{materia}/parciales/{anio}/{cuatrimestre}/{numero}.jpeg'.format(
            materia=self.materia.pk, anio=anio, cuatrimestre=cuatrimestre, numero=numero_parcial)
        self.assertEquals(expected, path)

    def test_file_path_de_recuperatorio(self):
        numero_parcial = 3
        cuatrimestre = ConjuntoDeEnunciadosConCuatrimestre.SEGUNDO
        anio = 2014
        parcial = Parcial(
            materia=self.materia, anio=anio, cuatrimestre=cuatrimestre, numero=numero_parcial,
            recuperatorio=True)
        path = conjunto_de_enunciados_file_path(parcial, 'archivo.rar')

        expected = '{materia}/recuperatorios/{anio}/{cuatrimestre}/{numero}.rar'.format(
            materia=self.materia.pk, anio=anio, cuatrimestre=cuatrimestre,
            numero=numero_parcial)
        self.assertEquals(expected, path)

    def test_file_path_de_final(self):
        fecha = date(1997, 4, 1)
        final = Final(materia=self.materia, fecha=fecha)
        path = conjunto_de_enunciados_file_path(final, 'archivo.pub')

        expected = '{materia}/finales/{fecha}.pub'.format(materia=self.materia.pk, fecha=fecha)
        self.assertEquals(expected, path)
