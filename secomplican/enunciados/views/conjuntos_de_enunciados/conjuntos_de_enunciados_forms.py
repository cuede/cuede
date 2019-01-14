from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from enunciados.models import ConjuntoDeEnunciadosConCuatrimestre, Final, \
    Parcial, Practica
from enunciados.utils import conjuntos_url_parser


class ConjuntoDeEnunciadosForm(forms.ModelForm):
    def __init__(self, materia_carrera, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.materia_carrera = materia_carrera
        self.instance.materia = materia_carrera.materia

    def _agregar_link_a_conjunto(self, mensaje):
        """Agrega el link al conjunto a un mensaje."""
        url = conjuntos_url_parser.url_conjunto(
            self.materia_carrera, self.instance)
        link = format_html('<a href="{}">{}</a>', url, self.instance)
        return mark_safe(mensaje + ' ' + link)

    def _agregar_link_a_conjunto_a_error(self):
        """
        Agrega el link al conjunto de enunciados en el error de code='exists'.
        """
        if self.has_error(NON_FIELD_ERRORS, 'exists'):
            errores = self.non_field_errors().as_data()
            error_exists = [
                error for error in errores if error.code == 'exists'
            ][0]
            viejo_mensaje = error_exists.message
            nuevo_mensaje = self._agregar_link_a_conjunto(viejo_mensaje)
            error_exists.message = nuevo_mensaje

    def is_valid(self):
        valid = super().is_valid()
        self._agregar_link_a_conjunto_a_error()
        return valid


class ConjuntoDeEnunciadosConCuatrimestreForm(ConjuntoDeEnunciadosForm):
    anio = forms.IntegerField(initial=timezone.now().year, label=_('Año'))
    cuatrimestre = forms.TypedChoiceField(
        choices=ConjuntoDeEnunciadosConCuatrimestre.NUMERO_CHOICES,
        widget=forms.RadioSelect, coerce=int, label=_('Cuatrimestre'))

    class Meta:
        fields = ['anio', 'cuatrimestre']


class PracticaForm(ConjuntoDeEnunciadosConCuatrimestreForm):
    numero = forms.IntegerField(initial=1, label=_('Número'))

    class Meta(ConjuntoDeEnunciadosConCuatrimestreForm.Meta):
        model = Practica
        fields = ConjuntoDeEnunciadosConCuatrimestreForm.Meta.fields + \
            ['numero']


class ParcialForm(ConjuntoDeEnunciadosConCuatrimestreForm):
    NUMERO_CHOICES = [
        (1, 'Primer parcial'),
        (2, 'Segundo parcial'),
        (3, 'Tercer parcial'),
    ]
    numero = forms.TypedChoiceField(
        choices=NUMERO_CHOICES, coerce=int, widget=forms.RadioSelect,
        label=_('Número'))

    class Meta(ConjuntoDeEnunciadosConCuatrimestreForm.Meta):
        model = Parcial
        fields = ConjuntoDeEnunciadosConCuatrimestreForm.Meta.fields + \
            ['numero', 'recuperatorio']


class FinalForm(ConjuntoDeEnunciadosForm):
    # Mostramos los últimos 50 años en el field de fecha, que vamos a
    # inicializar en el __init__.
    ANIOS = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tenemos que poner los años del field fecha dinámicamente.
        ahora = timezone.now()
        self.fields['fecha'] = forms.DateField(
            widget=forms.SelectDateWidget(
                years=range(ahora.year, ahora.year - self.ANIOS, -1),
            ), initial=ahora, label=_('Fecha'))

    class Meta:
        model = Final
        fields = ['fecha']
