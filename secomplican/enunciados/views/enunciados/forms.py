from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from enunciados.models import Enunciado, VersionTexto


class EnunciadoConConjuntoForm(forms.ModelForm):
    def __init__(self, conjunto, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conjunto = conjunto

    def is_valid(self):
        valid = super().is_valid()
        self.instance.conjunto = self.conjunto
        hubo_error = False
        try:
            self.instance.full_clean()
        except ValidationError as e:
            self.add_error(None, e)
            hubo_error = True
        return valid and not hubo_error

    class Meta:
        model = Enunciado
        fields = ['numero']
        labels = {
            'numero': gettext_lazy('Número')
        }


class VersionTextoForm(forms.ModelForm):
    class Meta:
        model = VersionTexto
        fields = ['texto']
