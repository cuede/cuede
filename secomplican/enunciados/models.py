from django.db import models

class Practica(models.Model):
    enunciados = models.ForeygnKey(Enunciado)
    materia = models.ForeignKey(Materia)
    # enunciados
    
class Enunciado(models.Model):
    practicas = models.ManyToManyField(Practica)
    texto = models.CharField()


class Materia(models.Model):
    nombre = models.CharField(max_length=1023)
    # practicas
