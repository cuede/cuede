from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from enunciados import cuatrimestres_url_parser
from enunciados.models import Materia, Enunciado, VersionTextoEnunciado, Cuatrimestre, Practica, Parcial, Final
from . import enunciados_utils


def render_enunciado(request, enunciado_elegido, url_solucion):
    contexto = {'enunciado': enunciado_elegido, 'url_solucion': url_solucion}
    return render(request, 'enunciados/enunciado.html', contexto)


def enunciado_practica(request, materia, anio, cuatrimestre, numero_practica, numero):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_practica(materia, anio, numero_cuatrimestre, numero_practica, numero)
    url_solucion = reverse('solucion_practica', kwargs={
        'materia': materia, 'anio': anio, 'cuatrimestre': cuatrimestre,
        'numero_practica': numero_practica,
        'numero': numero})
    return render_enunciado(request, encontrado, url_solucion)


def enunciado_parcial(request, materia, anio, cuatrimestre, numero_parcial, numero, es_recuperatorio):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_parcial(
        materia, anio, numero_cuatrimestre, numero_parcial, numero, es_recuperatorio)
    url_solucion = reverse('solucion_parcial', kwargs={
        'materia': materia, 'anio': anio, 'cuatrimestre': cuatrimestre,
        'numero_parcial': numero_parcial, 'numero': numero, 'es_recuperatorio': es_recuperatorio})
    return render_enunciado(request, encontrado, url_solucion)


def enunciado_final(request, materia, anio, mes, dia, numero):
    encontrado = enunciados_utils.enunciado_de_final(materia, anio, mes, dia, numero)
    url_solucion = reverse('solucion_final', kwargs={
        'materia': materia, 'anio': anio, 'mes': mes, 'dia': dia, 'numero': numero})
    return render_enunciado(request, encontrado, url_solucion)


class ConjuntoDeEnunciadosForm(forms.Form):
    PRACTICA = 0
    PARCIAL = 1
    FINAL = 2
    TIPO_CHOICES = [
        (PRACTICA, 'Práctica'),
        (PARCIAL, 'Parcial'),
        (FINAL, 'Final'),
    ]
    tipo = forms.ChoiceField(choices=TIPO_CHOICES)
    # Si es Parcial o Práctica necesitamos el año y el cuatrimestre
    anio = forms.IntegerField(initial=timezone.now().year)
    cuatrimestre = forms.ChoiceField(choices=Cuatrimestre.NUMERO_CHOICES, widget=forms.RadioSelect)
    # Si es Parcial, necesitamos el número de parcial, y saber si es un recu o no
    NUMERO_PARCIAL_CHOICES = [
        (1, 'Primer parcial'),
        (2, 'Segundo parcial'),
        (3, 'Tercer parcial'),
    ]
    numero_parcial = forms.ChoiceField(choices=NUMERO_PARCIAL_CHOICES, widget=forms.RadioSelect)
    es_recuperatorio = forms.BooleanField(required=False)
    # Si es Práctica, necesitamos el número de práctica
    numero_practica = forms.IntegerField(initial=1)
    # Si es final, necesitamos la fecha
    fecha = forms.DateField()

    def __init__(self, materia, data=None):
        self.materia = materia
        super().__init__(data)

    def _get_conjunto(self):
        """
        Devuelve el ConjuntoDeEnunciados que corresponde a los datos ingresados.

        Los datos se asumen que están en self.cleaned_data. Quizá se necesite llamar a
        super().clean() para esto primero.
        """
        tipo = int(self.cleaned_data.get('tipo'))
        if tipo == self.FINAL:
            fecha = self.cleaned_data.get('fecha')
            return Final(materia=self.materia, fecha=fecha)
        else:
            anio = self.cleaned_data.get('anio')
            cuatrimestre = int(self.cleaned_data.get('cuatrimestre'))
            objeto_cuatrimestre, created = Cuatrimestre.objects.get_or_create(anio=anio, numero=cuatrimestre)
            if tipo == self.PRACTICA:
                numero_practica = int(self.cleaned_data.get('numero_practica'))
                return Practica(materia=self.materia, cuatrimestre=objeto_cuatrimestre, numero=numero_practica)
            elif tipo == self.PARCIAL:
                numero_parcial = int(self.cleaned_data.get('numero_parcial'))
                es_recuperatorio = self.cleaned_data.get('es_recuperatorio')
                return Parcial(materia=self.materia, cuatrimestre=objeto_cuatrimestre, numero=numero_parcial,
                               recuperatorio=es_recuperatorio)
            else:
                # No deberíamos llegar nunca a esta parte, porque la verificación del tipo se hizo en el clean()
                raise VerificationError(_('El tipo no es válido.'))

    def clean(self):
        cleaned_data = super().clean()
        self._get_conjunto().full_clean()
        return cleaned_data

    def save(self, commit=True):
        conjunto = self._get_conjunto()
        if commit:
            conjunto.save()
        return conjunto


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
            # TODO Chequear que el numero de enunciado está bien, o sea, que no exista un enunciado
            # del conjunto que ya tenga el mismo número que éste.
            # Para eso se puede llamar directamente a Enunciado.full_clean() me parece.
            # TODO Chequear que el texto no sea vacío
            conjunto = conjunto_form.save()
            enunciado = enunciado_form.save(commit=False)
            enunciado.conjunto = conjunto
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
