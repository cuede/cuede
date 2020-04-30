import unittest

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

from enunciados.views.conjuntos_de_enunciados.validators.max_size_validator import \
    validate_max_size, MAX_FILE_SIZE


class MaxSizeValidatorTest(unittest.TestCase):
    def test_file_with_size_greater_than_max_should_not_validate(self):
        file = ContentFile('some content')
        file.size = MAX_FILE_SIZE + 1
        try:
            validate_max_size(file)
            self.fail('ValidationError should be raised')
        except ValidationError:
            pass

    def test_file_with_size_smaller_than_max_should_validate(self):
        file = ContentFile('some content')
        file.size = MAX_FILE_SIZE - 1

        validate_max_size(file)

    def test_file_with_max_size_should_validate(self):
        file = ContentFile('some content')
        file.size = MAX_FILE_SIZE

        validate_max_size(file)
