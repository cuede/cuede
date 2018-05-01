from django.db import models


class Materia(models.Model):
    nombre = models.CharField(max_length=1023)


# No estoy seguro de que Etapa haga falta, podemos simplemente poner los datos de la etapa
# en cada practica o parcial.
class Etapa(models.Model):
    """
    Representa la etapa de un año: 1er cuatrimestre, 2do cuatrimestre, o verano.
    """
    anio = models.IntegerField()
    # 1 = 1er cuatrimestre, 2 = 2do cuatrimestre, 3 = verano
    # Quiza haya una forma mas linda de representar en que cuatri estamos.
    cuatrimestre = models.IntegerField()


class Practica(models.Model):
    materia = models.ForeignKey(Materia, models.CASCADE)
    etapa = models.ForeignKey(Etapa, models.CASCADE)


class Enunciado(models.Model):
    practica = models.ForeignKey(Practica, models.CASCADE)
    texto = models.TextField()


class Solucion(models.Model):
    enunciado = models.ForeignKey(Enunciado, models.CASCADE)
    texto = models.TextField()
