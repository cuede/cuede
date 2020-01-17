from django.forms import ModelForm, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.db.models import F

from enunciados.models import Solucion, VersionTexto
from enunciados.utils import enunciados_url_parser
from enunciados.views.breadcrumb import breadcrumb_editar_solucion


PUNTOS_USUARIO_POR_EDITAR_SOLUCION = 5


class VersionTextoSolucionForm(ModelForm):
    def __init__(self, solucion, autor, *args, **kwargs):
        self.solucion = solucion
        self.autor = autor
        super().__init__(*args, **kwargs)

    def clean_texto(self):
        texto_anterior = self.solucion.versiones.ultima().texto
        texto_nuevo = self.cleaned_data['texto']
        if texto_nuevo == texto_anterior:
            raise ValidationError(_('No se cambió el texto.'))
        return texto_nuevo

    def save(self):
        self.instance.posteo = self.solucion
        self.instance.autor = self.autor
        return super().save()

    class Meta:
        model = VersionTexto
        fields = ['texto']


def no_edito_solucion(solucion, usuario):
    return solucion.versiones.filter(autor=usuario).count() == 0


def dar_puntos_a_usuario(usuario):
    informacion_usuario = usuario.informacionusuario
    informacion_usuario.puntos = F('puntos') + PUNTOS_USUARIO_POR_EDITAR_SOLUCION
    informacion_usuario.save()


@login_required
def editar_solucion(request, pk_solucion, **kwargs):
    materia_carrera = kwargs['materia_carrera']
    solucion = get_object_or_404(Solucion, pk=pk_solucion)
    usuario = request.user
    if request.method == 'POST':
        form = VersionTextoSolucionForm(solucion, usuario, request.POST)
        if form.is_valid():
            deberia_sumar_puntos = no_edito_solucion(solucion, usuario)
            form.save()
            if deberia_sumar_puntos:
                dar_puntos_a_usuario(usuario)
            success_url = enunciados_url_parser.url_enunciado(
                materia_carrera, solucion.enunciado_padre)
            return redirect(success_url)
    else:
        form = VersionTextoSolucionForm(
            solucion, usuario, initial={'texto': solucion.versiones.ultima().texto})

    contexto = {
        'materia_carrera': materia_carrera,
        'carrera': materia_carrera.carrera,
        'form': form,
        'solucion': solucion,
        'enunciado': solucion.enunciado_padre,
        'breadcrumb': breadcrumb_editar_solucion(
            materia_carrera, solucion.enunciado_padre),
        'texto_boton': _('Enviar'),
    }
    return render(request, 'enunciados/nueva_solucion.html', contexto)
