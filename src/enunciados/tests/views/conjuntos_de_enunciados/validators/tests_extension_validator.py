import unittest

from enunciados.views.conjuntos_de_enunciados.validators.extension_validator import \
    is_extension_correct


class ExtensionValidatorTest(unittest.TestCase):
    def test_extension_corresponding_to_mime_type_is_correct(self):
        self.assertTrue(is_extension_correct('archivo.pdf', 'application/pdf'))

    def test_extension_not_corresponding_to_mime_type_is_not_correct(self):
        self.assertFalse(is_extension_correct('archivo.gif', 'application/pdf'))



