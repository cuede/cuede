from unittest import TestCase
from enunciados.string_utils import *


def generar_texto(caracteres):
    """Devuelve un texto con ``caracteres`` cantidad de caracteres."""
    return 'a' * caracteres


class StringUtilsTests(TestCase):
    def test_truncar_con_texto_de_menos_de_32_caracteres(self):
        """No debería truncarlo."""
        texto = generar_texto(10)
        self.assertEquals(truncar(texto), texto)

    def test_truncar_con_texto_de_32_caracteres(self):
        """No debería truncarlo."""
        texto = generar_texto(32)
        self.assertEquals(truncar(texto), texto)

    def test_truncar_con_texto_de_mas_de_32_caracteres(self):
        """Debería truncarlo"""
        texto = generar_texto(33)
        texto_truncado = texto[:29] + '...'
        self.assertEquals(truncar(texto), texto_truncado)

    def test_truncar_con_max_caracteres(self):
        """Debería respetar la cantidad de caracteres"""
        max_caracteres = 42
        texto = generar_texto(max_caracteres)
        self.assertEquals(truncar(texto, max_caracteres), texto)
        texto += 'a'
        texto_truncado = texto[:39] + '...'
        self.assertEquals(truncar(texto, max_caracteres), texto_truncado)
