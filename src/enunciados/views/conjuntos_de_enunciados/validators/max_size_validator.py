from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 2 * 1024 * 1024


def validate_max_size(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError('El archivo no puede tener más de 2MB')
