import unittest

from enunciados.views.conjuntos_de_enunciados.validators.mimetype_validator import \
    is_valid_mime_type


class MimeTypeValidatorTest(unittest.TestCase):
    def test_pdf_is_valid_mime_type(self):
        self.assertTrue(is_valid_mime_type('application/pdf'))

    def test_any_image_mime_type_is_valid(self):
        self.assertTrue(is_valid_mime_type('image/bmp'))
        self.assertTrue(is_valid_mime_type('image/gif'))
        self.assertTrue(is_valid_mime_type('image/pepito'))

    def test_any_other_mime_type_is_not_valid(self):
        self.assertFalse(is_valid_mime_type('application/octet-stream'))
