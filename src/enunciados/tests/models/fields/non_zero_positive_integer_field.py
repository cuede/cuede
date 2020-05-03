from django.core.exceptions import ValidationError
from django.db.models import PositiveIntegerField
from django.utils.translation import gettext_lazy as _


def validate_positive_number(number):
    if number <= 0:
        raise ValidationError(
            _('El número %(number)s no es positivo.'),
            code='non_positive_number',
            params={'number': number}
        )


class NonZeroPositiveIntegerField(PositiveIntegerField):
    description = _("Non zero positive integer")
    default_validators = [validate_positive_number]

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 1,
            **kwargs,
        })
