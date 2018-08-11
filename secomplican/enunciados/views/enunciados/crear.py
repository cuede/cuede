from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from enunciados.models import (ConjuntoDeEnunciadosConCuatrimestre, Enunciado,
                               Final, Materia, Parcial, Practica,
                               VersionTextoEnunciado)


class ConjuntoDeEnunciadosForm(forms.Form):
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
    # Si es Práctica, necesitamos el número de práctica
    numero_practica = forms.IntegerField(initial=1, required=False)
    # Si es final, necesitamos la fecha
    fecha = forms.DateField(required=False)

    def __init__(self, materia, data=None):
        self.materia = materia
        super().__init__(data)

    def _get_conjunto(self):
        """
        Devuelve el ConjuntoDeEnunciados que corresponde a los datos ingresados, junto con un booleano que dice si
        es un objeto nuevo. Si ya existe, toma ese, sino crea uno nuevo pero sin guardarlo.

        Los datos se asumen que están en self.cleaned_data. Quizá se necesite llamar a
        super().clean() para esto primero.
        """
        creado = False
        tipo = self.cleaned_data.get('tipo')
        if tipo == self.FINAL:
            fecha = self.cleaned_data.get('fecha')
            try:
                conjunto = Final.objects.get(materia=self.materia, fecha=fecha)
            except Final.DoesNotExist:
                conjunto = Final(materia=self.materia, fecha=fecha)
                creado = True
        else:
            anio = self.cleaned_data.get('anio')
            cuatrimestre = self.cleaned_data.get('cuatrimestre')
            if tipo == self.PRACTICA:
                numero_practica = self.cleaned_data.get('numero_practica')
                try:
                    conjunto = Practica.objects.get(materia=self.materia, cuatrimestre=cuatrimestre,
                                                    anio=anio, numero=numero_practica)
                except Practica.DoesNotExist:
                    conjunto = Practica(materia=self.materia, anio=anio, cuatrimestre=cuatrimestre,
                                        numero=numero_practica)
                    creado = True

            elif tipo == self.PARCIAL:
                numero_parcial = self.cleaned_data.get('numero_parcial')
                es_recuperatorio = self.cleaned_data.get('es_recuperatorio')
                try:
                    conjunto = Parcial.objects.get(materia=self.materia, anio=anio, cuatrimestre=cuatrimestre,
                                                   numero=numero_parcial, recuperatorio=es_recuperatorio)
                except Parcial.DoesNotExist:
                    conjunto = Parcial(materia=self.materia, anio=anio, cuatrimestre=cuatrimestre,
                                       numero=numero_parcial, recuperatorio=es_recuperatorio)
                    creado = True
            else:
                # No deberíamos llegar nunca a esta parte, porque la verificación del tipo se hizo en el clean()
                raise ValidationError(_('El tipo no es válido.'))

        return conjunto, creado

    def clean(self):
        cleaned_data = super().clean()
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


def nuevo_enunciado(request, materia):
    objeto_materia = get_object_or_404(Materia, nombre=materia)
    if request.method == 'POST':
        conjunto_form = ConjuntoDeEnunciadosForm(objeto_materia, request.POST)
        enunciado_form = EnunciadoForm(request.POST)
        version_texto_form = VersionTextoForm(request.POST)
        if conjunto_form.is_valid() and enunciado_form.is_valid() and version_texto_form.is_valid():
            # TODO Chequear que el texto no sea vacío
            conjunto, creado = conjunto_form.save()
            enunciado = enunciado_form.save(commit=False)
            enunciado.conjunto = conjunto
            hubo_error = False
            if not creado:
                # Hace falta fijarse si el número del enunciado está bien.
                # Eso se puede hacer directamente llamando a full_clean().
                try:
                    enunciado.full_clean()
                except ValidationError as error:
                    enunciado_form.add_error(None, error)
                    hubo_error = True

            if not hubo_error:
                enunciado.save()
                version_texto = version_texto_form.save(commit=False)
                version_texto.enunciado = enunciado
                version_texto.save()
                return redirect(enunciado.get_absolute_url())
    else:
        conjunto_form = ConjuntoDeEnunciadosForm(objeto_materia)
        enunciado_form = EnunciadoForm()
        version_texto_form = VersionTextoForm()

    context = {'conjunto_form': conjunto_form, 'enunciado_form': enunciado_form,
               'version_texto_form': version_texto_form}
    return render(request, 'enunciados/nuevo_enunciado.html', context)
