from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from enunciados.modelmanagers.versiones_manager import VersionesManager


class Materia(models.Model):
    pass


class ConjuntoDeEnunciados(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)


class ConjuntoDeEnunciadosConCuatrimestre(ConjuntoDeEnunciados):
    anio = models.IntegerField()

    VERANO = 0
    PRIMERO = 1
    SEGUNDO = 2
    TEXTOS_CUATRIMESTRE = {
        PRIMERO: _('Primer Cuatrimestre'),
        SEGUNDO: _('Segundo Cuatrimestre'),
        VERANO: _('Verano'),
    }
    NUMERO_CHOICES = (
        (VERANO, TEXTOS_CUATRIMESTRE[VERANO]),
        (PRIMERO, TEXTOS_CUATRIMESTRE[PRIMERO]),
        (SEGUNDO, TEXTOS_CUATRIMESTRE[SEGUNDO]),
    )

    cuatrimestre = models.IntegerField(choices=NUMERO_CHOICES)

    class Meta:
        abstract = True


class Practica(ConjuntoDeEnunciadosConCuatrimestre):
    numero = models.IntegerField()
    titulo = models.CharField(max_length=1023, default='', blank=True)

    def __str__(self):
        from enunciados.utils import cuatrimestres_parser
        texto_cuatrimestre = cuatrimestres_parser.numero_a_texto(
            self.cuatrimestre)
        return 'Práctica {} del {} del {}'.format(self.numero, texto_cuatrimestre, self.anio)

    def clean(self):
        # Ver que no haya ya una Practica con iguales atributos
        if Practica.objects.filter(
                materia=self.materia, anio=self.anio,
                cuatrimestre=self.cuatrimestre, numero=self.numero).exists():
            raise ValidationError(
                _('Ya hay una Práctica con estos atributos.'),
                code='exists'
            )


class Parcial(ConjuntoDeEnunciadosConCuatrimestre):
    numero = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    recuperatorio = models.BooleanField(default=False)

    def __str__(self):
        from enunciados.utils import cuatrimestres_parser
        texto_cuatrimestre = cuatrimestres_parser.numero_a_texto(
            self.cuatrimestre)
        nombre = 'Parcial'
        if self.recuperatorio:
            nombre = 'Recuperatorio'
        return '{} {} del {} del {}'.format(self.ordinal()['singular'], nombre, texto_cuatrimestre, self.anio)

    def clean(self):
        # Ver que no haya ya un Parcial con iguales atributos
        if Parcial.objects.filter(
                materia=self.materia, anio=self.anio,
                cuatrimestre=self.cuatrimestre, numero=self.numero,
                recuperatorio=self.recuperatorio).exists():
            raise ValidationError(
                _('Ya hay un Parcial con estos atributos.'),
                code='exists'
            )

    def ordinal(self):
        """
        Devuelve el adjetivo ordinal correspondiente al número de este parcial,
        tanto en singular como en plural.
        """
        # Asumimos que no hay mas de cuatro parciales. Deberíamos quizá usar una library que te provea los ordinales.
        ordinales = [
            {'singular': 'Primer', 'plural': 'Primeros'},
            {'singular': 'Segundo', 'plural': 'Segundos'},
            {'singular': 'Tercer', 'plural': 'Terceros'},
            {'singular': 'Cuarto', 'plural': 'Cuartos'},
        ]
        if self.numero > len(ordinales):
            return {'singular': 'N-avo', 'plural': 'N-avos'}
        else:
            return ordinales[self.numero - 1]


class Final(ConjuntoDeEnunciados):
    fecha = models.DateField()

    def __str__(self):
        return 'Final del {}'.format(self.fecha)

    def clean(self):
        # Ver que no haya ya un final con igual fecha y materia
        if Final.objects.filter(materia=self.materia, fecha=self.fecha).exists():
            raise ValidationError(
                _('Ya hay un Final con esta materia y fecha.'),
                code='exists'
            )


class Enunciado(models.Model):
    conjunto = models.ForeignKey(
        ConjuntoDeEnunciados, on_delete=models.CASCADE)
    # El numero de enunciado en el conjunto de enunciados.
    numero = models.IntegerField()
    votos = models.IntegerField(default=0)

    def __str__(self):
        return 'Ejercicio {}'.format(self.numero)

    class Meta:
        ordering = ['numero']
        # No puede haber dos ejercicios con el mismo número en el mismo conjunto.
        unique_together = ('numero', 'conjunto')


class VersionTexto(models.Model):
    tiempo = models.DateTimeField(auto_now_add=True)
    texto = models.TextField(blank=False)
    versiones = VersionesManager()

    def __str__(self):
        return self.texto

    class Meta:
        # Ordenamos del más reciente al más viejo.
        ordering = ['-tiempo']
        abstract = True


class VersionTextoEnunciado(VersionTexto):
    enunciado = models.ForeignKey(
        Enunciado, on_delete=models.CASCADE, related_name='versiones')


class Solucion(models.Model):
    enunciado = models.ForeignKey(
        Enunciado, on_delete=models.CASCADE, related_name='soluciones')

    def __str__(self):
        return str(self.versiones.ultima())


class VersionTextoSolucion(VersionTexto):
    solucion = models.ForeignKey(
        Solucion, on_delete=models.CASCADE, related_name='versiones')


class InformacionUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntos = models.PositiveIntegerField(default=0)
    votos_enunciados = models.ManyToManyField(Enunciado, through='VotoEnunciado')


class VotoEnunciado(models.Model):
    usuario = models.ForeignKey(InformacionUsuario, on_delete=models.CASCADE)
    enunciado = models.ForeignKey(Enunciado, on_delete=models.CASCADE)
    positivo = models.BooleanField()
