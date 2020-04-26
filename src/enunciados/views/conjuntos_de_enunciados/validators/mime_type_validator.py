import magic
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_allowed_mime_type(file):
    mime_type = get_mime_type(file)
    if not is_valid_mime_type(mime_type):
        raise ValidationError(
            _("El archivo no puede tener tipo %(mime_type)s, solo puede ser "
              "un PDF o una imagen."),
            code='invalid_mime_type',
            params={'mime_type': mime_type},
        )


def get_mime_type(file):
    return magic.from_buffer(file.read(2048), mime=True)


def is_valid_mime_type(mime_type):
    return is_pdf_mime_type(mime_type) or is_image_mime_type(mime_type)


def is_pdf_mime_type(mime_type):
    return mime_type == 'application/pdf'


def is_image_mime_type(mime_type):
    return mime_type.startswith('image/')
