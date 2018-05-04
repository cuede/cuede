from django.db import models
from enunciados.string_utils import truncar


class Materia(models.Model):
    nombre = models.CharField(max_length=1023)

    def __str__(self):
        return self.nombre


class Cuatrimestre(models.Model):
    """
    Representa la etapa de un año: 1er cuatrimestre, 2do cuatrimestre, o verano.
    """
    anio = models.IntegerField()

    PRIMERO = 1
    SEGUNDO = 2
    VERANO = 3
    CUATRIMESTRE_CHOICES = (
        (PRIMERO, 'Primer Cuatrimestre'),
        (SEGUNDO, 'Segundo Cuatrimestre'),
        (VERANO, 'Verano')
    )

    cuatrimestre = models.IntegerField(choices=CUATRIMESTRE_CHOICES)

    def __str_cuatrimestre(self):
        if self.cuatrimestre == self.PRIMERO:
            return 'Primer Cuatrimestre'
        elif self.cuatrimestre == self.SEGUNDO:
            return 'Segundo Cuatrimestre'
        else:
            return 'Verano'

    def __str__(self):
        return '{} del {}'.format(self.__str_cuatrimestre(), self.anio)


class ConjuntoDeEnunciados(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    cuatrimestre = models.ForeignKey(Cuatrimestre, on_delete=models.CASCADE)


class Practica(ConjuntoDeEnunciados):
    numero = models.IntegerField()
    titulo = models.CharField(max_length=1023, default='')

    def __str__(self):
        resultado = 'Practica {}'.format(self.numero)
        if self.titulo != '':
            resultado += ': {}'.format(self.titulo)
        return resultado


class Parcial(ConjuntoDeEnunciados):
    numero = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    recuperatorio = models.BooleanField(default=False)

    def __str__(self):
        template = 'Parcial {}'
        if self.recuperatorio:
            template = 'Recuperatorio {}'
        return template.format(self.numero)


class Enunciado(models.Model):
    conjunto = models.ForeignKey(ConjuntoDeEnunciados, on_delete=models.CASCADE)
    # El numero de enunciado en la practica
    numero = models.IntegerField()
    texto = models.TextField()

    def __str__(self):
        return truncar(self.texto)

    class Meta:
        ordering = ['numero']


class Solucion(models.Model):
    enunciado = models.ForeignKey(Enunciado, on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return truncar(self.texto)
