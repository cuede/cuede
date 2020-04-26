from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import humanize


MAX_FILE_SIZE = 2 * 1024 * 1024


def validate_max_size(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(
            _('El archivo no puede tener más de 2 MiB; tiene %(size)s.'),
            code='invalid_file_size',
            params={'size': humanize.naturalsize(file.size, binary=True)},
        )
