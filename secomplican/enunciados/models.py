from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


from enunciados.modelmanagers.versiones_manager import VersionesManager


class Materia(models.Model):
    NOMBRE_MAX_LENGTH = 1023
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    slug = models.SlugField(max_length=NOMBRE_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('materia', kwargs={'nombre': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        # TODO Fijarse que no haya dos materias con slug iguales.
        super().save(*args, **kwargs)


class ConjuntoDeEnunciados(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)


class ConjuntoDeEnunciadosConCuatrimestre(ConjuntoDeEnunciados):
    anio = models.IntegerField()

    PRIMERO = 1
    SEGUNDO = 2
    VERANO = 3
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
        from enunciados import cuatrimestres_parser
        texto_cuatrimestre = cuatrimestres_parser.numero_a_texto(self.cuatrimestre)
        return 'Práctica {} del {} del {}'.format(self.numero, texto_cuatrimestre, self.anio)

    def get_absolute_url(self):
        from enunciados import cuatrimestres_url_parser
        kwargs = {
            'materia': self.materia.nombre,
            'anio': self.anio,
            'cuatrimestre': cuatrimestres_url_parser.numero_a_url(self.cuatrimestre),
            'numero': self.numero
        }
        return reverse('practica', kwargs=kwargs)


class Parcial(ConjuntoDeEnunciadosConCuatrimestre):
    numero = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    recuperatorio = models.BooleanField(default=False)

    def __str__(self):
        from enunciados import cuatrimestres_parser
        texto_cuatrimestre = cuatrimestres_parser.numero_a_texto(self.cuatrimestre)
        nombre = 'Parcial'
        if self.recuperatorio:
            nombre = 'Recuperatorio'
        return '{} {} del {} del {}'.format(self.ordinal()['singular'], nombre, texto_cuatrimestre, self.anio)

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

    def get_absolute_url(self):
        from enunciados import cuatrimestres_url_parser
        kwargs = {
            'materia': self.materia.nombre,
            'anio': self.anio,
            'cuatrimestre': cuatrimestres_url_parser.numero_a_url(self.cuatrimestre),
            'numero': self.numero
        }
        if self.recuperatorio:
            return reverse('recuperatorio', kwargs=kwargs)
        else:
            return reverse('parcial', kwargs=kwargs)


class Final(ConjuntoDeEnunciados):
    fecha = models.DateField()

    def __str__(self):
        return 'Final del {}'.format(self.fecha)

    def get_absolute_url(self):
        kwargs = {
            'materia': self.materia.nombre,
            'anio': self.fecha.year,
            'mes': self.fecha.month,
            'dia': self.fecha.day,
        }
        return reverse('final', kwargs=kwargs)

    def clean(self):
        # Ver que no haya ya un final con igual fecha y materia
        if Final.objects.filter(materia=self.materia, fecha=self.fecha).exists():
            raise ValidationError(_('Ya hay un Final con esta materia y fecha.'))


class Enunciado(models.Model):
    conjunto = models.ForeignKey(ConjuntoDeEnunciados, on_delete=models.CASCADE)
    # El numero de enunciado en el conjunto de enunciados.
    numero = models.IntegerField()

    def __str__(self):
        return 'Enunciado {}'.format(self.numero)

    def get_absolute_url(self):
        from . import cuatrimestres_url_parser
        kwargs = {
            'materia': self.conjunto.materia.nombre,
            'numero': self.numero,
        }

        # Esto es horrible, pero no sé si hay otra forma de chequear de qué subtipo es el conjunto.
        try:
            parcial = self.conjunto.parcial
            kwargs['numero_parcial'] = parcial.numero
            kwargs['anio'] = parcial.anio
            kwargs['cuatrimestre'] = cuatrimestres_url_parser.numero_a_url(parcial.cuatrimestre)
            if parcial.recuperatorio:
                url = 'enunciado_recuperatorio'
            else:
                url = 'enunciado_parcial'
        except Parcial.DoesNotExist:
            try:
                practica = self.conjunto.practica
                kwargs['numero_practica'] = practica.numero
                kwargs['anio'] = practica.anio
                kwargs['cuatrimestre'] = cuatrimestres_url_parser.numero_a_url(practica.cuatrimestre)
                url = 'enunciado_practica'
            except Practica.DoesNotExist:
                try:
                    final = self.conjunto.final
                    kwargs['anio'] = final.fecha.year
                    kwargs['mes'] = final.fecha.month
                    kwargs['dia'] = final.fecha.day
                    url = 'enunciado_final'
                except Final.DoesNotExist:
                    raise Exception('El Enunciado no tiene un tipo de ConjuntoDeEnunciados conocido.')

        return reverse(url, kwargs=kwargs)

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
    enunciado = models.ForeignKey(Enunciado, on_delete=models.CASCADE, related_name='versiones')


class Solucion(models.Model):
    enunciado = models.ForeignKey(Enunciado, on_delete=models.CASCADE, related_name='soluciones')

    def __str__(self):
        return str(self.versiones.ultima())


class VersionTextoSolucion(VersionTexto):
    solucion = models.ForeignKey(Solucion, on_delete=models.CASCADE, related_name='versiones')
