from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from enunciados.models import (Materia, ConjuntoDeEnunciadosConCuatrimestre,
                               Enunciado, Final, Parcial, Practica,
                               VersionTextoEnunciado)


class ConjuntoDeEnunciadosForm(forms.Form):
    materia = forms.ModelChoiceField(
        queryset=Materia.objects.all(),
        empty_label=None,
        to_field_name='slug')

    PRACTICA = 0
    PARCIAL = 1
    FINAL = 2
    TIPO_CHOICES = [
        (PRACTICA, 'Práctica'),
        (PARCIAL, 'Parcial'),
        (FINAL, 'Final'),
    ]
    tipo = forms.TypedChoiceField(choices=TIPO_CHOICES, coerce=int)
    # Si es Parcial o Práctica necesitamos el año y el cuatrimestre
    anio = forms.IntegerField(initial=timezone.now().year, required=False)
    cuatrimestre = forms.TypedChoiceField(choices=ConjuntoDeEnunciadosConCuatrimestre.NUMERO_CHOICES,
                                          widget=forms.RadioSelect, coerce=int, required=False)
    # Si es Parcial, necesitamos el número de parcial, y saber si es un recu o no
    NUMERO_PARCIAL_CHOICES = [
        (1, 'Primer parcial'),
        (2, 'Segundo parcial'),
        (3, 'Tercer parcial'),
    ]
    numero_parcial = forms.TypedChoiceField(
        choices=NUMERO_PARCIAL_CHOICES, coerce=int, widget=forms.RadioSelect, required=False)
    es_recuperatorio = forms.BooleanField(required=False)
    # Si es Práctica, necesitamos el número de práctica.
    numero_practica = forms.IntegerField(initial=1, required=False)
    # Mostramos los últimos 50 años en el field de fecha, que vamos a
    # inicializar en el __init__.
    ANIOS = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es final, necesitamos la fecha.
        # Tenemos que poner los años del field fecha dinámicamente.
        ahora = timezone.now()
        self.fields['fecha'] = forms.DateField(
            widget=forms.SelectDateWidget(
                years=range(ahora.year, ahora.year - self.ANIOS, -1),
            ), initial=ahora, required=False)

    def _get_conjunto(self):
        """
        Devuelve el ConjuntoDeEnunciados que corresponde a los datos ingresados, junto con un booleano que dice si
        es un objeto nuevo. Si ya existe, toma ese, sino crea uno nuevo pero sin guardarlo.

        Los datos se asumen que están en self.cleaned_data. Quizá se necesite llamar a
        super().clean() para esto primero.
        """
        creado = False
        materia = self.cleaned_data.get('materia')
        tipo = self.cleaned_data.get('tipo')
        if tipo == self.FINAL:
            fecha = self.cleaned_data.get('fecha')
            try:
                conjunto = Final.objects.get(materia=materia, fecha=fecha)
            except Final.DoesNotExist:
                conjunto = Final(materia=materia, fecha=fecha)
                creado = True
        else:
            anio = self.cleaned_data.get('anio')
            cuatrimestre = self.cleaned_data.get('cuatrimestre')
            if tipo == self.PRACTICA:
                numero_practica = self.cleaned_data.get('numero_practica')
                try:
                    conjunto = Practica.objects.get(materia=materia, cuatrimestre=cuatrimestre,
                                                    anio=anio, numero=numero_practica)
                except Practica.DoesNotExist:
                    conjunto = Practica(materia=materia, anio=anio, cuatrimestre=cuatrimestre,
                                        numero=numero_practica)
                    creado = True

            elif tipo == self.PARCIAL:
                numero_parcial = self.cleaned_data.get('numero_parcial')
                es_recuperatorio = self.cleaned_data.get('es_recuperatorio')
                try:
                    conjunto = Parcial.objects.get(materia=materia, anio=anio, cuatrimestre=cuatrimestre,
                                                   numero=numero_parcial, recuperatorio=es_recuperatorio)
                except Parcial.DoesNotExist:
                    conjunto = Parcial(materia=materia, anio=anio, cuatrimestre=cuatrimestre,
                                       numero=numero_parcial, recuperatorio=es_recuperatorio)
                    creado = True
            else:
                # No deberíamos llegar nunca a esta parte, porque la verificación del tipo se hizo en el clean()
                raise ValidationError(_('El tipo no es válido.'))

        return conjunto, creado

    def _revisar_presente(self, field):
        presente = True
        valor = self.cleaned_data.get(field)
        if not valor:
            self.add_error(field, ValidationError(
                _('Se necesita ' + field + '.')))
            presente = False
        return presente

    def _revisar_suficiente_informacion(self):
        """Verifica que hay suficiente información para poder crear un conjunto del tipo pedido."""
        tipo = self.cleaned_data.get('tipo')
        if tipo == self.FINAL:
            hay_suficiente_informacion = self._revisar_presente('fecha')
        else:
            hay_suficiente_informacion = self._revisar_presente('anio')
            hay_suficiente_informacion = (hay_suficiente_informacion and
                                          self._revisar_presente('cuatrimestre'))
            if tipo == self.PRACTICA:
                hay_suficiente_informacion = (hay_suficiente_informacion and
                                              self._revisar_presente('numero_practica'))
            elif tipo == self.PARCIAL:
                hay_suficiente_informacion = (hay_suficiente_informacion and
                                              self._revisar_presente('numero_parcial'))
            else:
                # No deberíamos llegar nunca a esta parte, porque la verificación del tipo se hizo en el clean()
                raise ValidationError(_('El tipo no es válido.'))
        return hay_suficiente_informacion

    def clean(self):
        cleaned_data = super().clean()
        if self._revisar_suficiente_informacion():
            conjunto, creado = self._get_conjunto()
            if creado:
                conjunto.full_clean()
        return cleaned_data

    def save(self, commit=True):
        """
        Devuelve el conjunto que corresponde a los datos de este Form, y lo guarda si no existe y si commit=True.
        El segundo valor retornado es un booleano que indica si se tuvo que crear un nuevo conjunto.
        """
        conjunto, creado = self._get_conjunto()
        if commit and creado:
            conjunto.save()
        return conjunto, creado


class EnunciadoForm(forms.ModelForm):
    class Meta:
        model = Enunciado
        fields = ['numero']


class VersionTextoForm(forms.ModelForm):
    class Meta:
        model = VersionTextoEnunciado
        fields = ['texto']
