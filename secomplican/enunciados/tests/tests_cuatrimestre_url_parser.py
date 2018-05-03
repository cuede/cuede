from django.test import TestCase
from enunciados.cuatrimestres_url_parser import *


# Create your tests here.
class CuatrimestresUrlParserTests(TestCase):
    def test_numero_a_url_con_numeros_validos(self):
        """
        Debería devolver la parte de la url correspondiente.
        """
        self.assertEquals(numero_a_url(1), '1cuatri')
        self.assertEquals(numero_a_url(2), '2cuatri')
        self.assertEquals(numero_a_url(3), 'verano')

    def test_numero_a_url_con_numeros_invalidos(self):
        """
        Debería devolver None.
        """
        self.assertIsNone(numero_a_url(4))

    def test_url_a_numero_con_urls_validas(self):
        """
        Debería devolver los números correspondientes.
        """
        self.assertEquals(url_a_numero('1cuatri'), 1)
        self.assertEquals(url_a_numero('2cuatri'), 2)
        self.assertEquals(url_a_numero('verano'), 3)

    def test_url_a_numero_con_url_invalida(self):
        """
        Debería devolver None.
        """
        self.assertIsNone(url_a_numero('invalida'))


