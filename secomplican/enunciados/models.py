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
    NUMERO_CHOICES = (
        (PRIMERO, 'Primer Cuatrimestre'),
        (SEGUNDO, 'Segundo Cuatrimestre'),
        (VERANO, 'Verano')
    )

    numero = models.IntegerField(choices=NUMERO_CHOICES)

    def __str_cuatrimestre(self):
        if self.numero == self.PRIMERO:
            return 'Primer Cuatrimestre'
        elif self.numero == self.SEGUNDO:
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
        return '{} - Practica {} del {}'.format(self.materia, self.numero, self.cuatrimestre)


class Parcial(ConjuntoDeEnunciados):
    numero = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    recuperatorio = models.BooleanField(default=False)

    def __str__(self):
        nombre = 'Parcial'
        if self.recuperatorio:
            nombre = 'Recuperatorio'
        return '{} - {} {} del {}'.format(self.materia, nombre, self.numero, self.cuatrimestre)


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
