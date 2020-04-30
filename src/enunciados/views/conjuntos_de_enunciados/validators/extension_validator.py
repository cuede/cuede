import mimetypes
import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from enunciados.views.conjuntos_de_enunciados.validators.mime_type_validator import get_mime_type


def is_extension_correct(filename, mime_type):
    return mimetypes.guess_type(filename)[0] == mime_type


def validate_extension(file):
    mime_type = get_mime_type(file)
    if not is_extension_correct(file.name, mime_type):
        raise ValidationError(
            _('La extensión "%(extension)s" del archivo no corresponde con su tipo "%(mime_type)s".'),
            code='invalid_extension',
            params={'extension': os.path.splitext(file.name)[1], 'mime_type': mime_type}
        )
