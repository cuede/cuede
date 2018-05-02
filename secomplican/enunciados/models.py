from django.db import models
from enum import Enum
from enunciados.string_utils import truncar


class Materia(models.Model):
    nombre = models.CharField(max_length=1023)

    def __str__(self):
        return self.nombre


# No estoy seguro de que Etapa haga falta, podemos simplemente poner los datos de la etapa
# en cada practica o parcial.
class Etapa(models.Model):
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


class Practica(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)
    numero = models.IntegerField()
    titulo = models.CharField(max_length=1023, default='')

    def __str__(self):
        resultado = 'Practica {}'.format(self.numero)
        if self.titulo != '':
            resultado += ': {}'.format(self.titulo)
        return resultado


class Enunciado(models.Model):
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return truncar(self.texto)


class Solucion(models.Model):
    enunciado = models.ForeignKey(Enunciado, on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return truncar(self.texto)
