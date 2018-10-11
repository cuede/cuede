from django import forms
from django.utils import timezone

from enunciados.models import (ConjuntoDeEnunciadosConCuatrimestre, Final,
                               Parcial, Practica)


class ConjuntoDeEnunciadosForm(forms.ModelForm):
    def __init__(self, materia, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.materia = materia


class ConjuntoDeEnunciadosConCuatrimestreForm(ConjuntoDeEnunciadosForm):
    anio = forms.IntegerField(initial=timezone.now().year)
    cuatrimestre = forms.TypedChoiceField(
        choices=ConjuntoDeEnunciadosConCuatrimestre.NUMERO_CHOICES,
        widget=forms.RadioSelect, coerce=int)

    class Meta:
        fields = ['anio', 'cuatrimestre']


class PracticaForm(ConjuntoDeEnunciadosConCuatrimestreForm):
    numero = forms.IntegerField(initial=1)

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
        choices=NUMERO_CHOICES, coerce=int, widget=forms.RadioSelect)

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
            ), initial=ahora)

    class Meta:
        model = Final
        fields = ['fecha']
