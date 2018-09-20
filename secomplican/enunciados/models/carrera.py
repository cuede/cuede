from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from enunciados.models.models import Materia

NOMBRE_MAX_LENGTH = 1023


class Universidad(models.Model):
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    slug = models.SlugField(max_length=NOMBRE_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    slug = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia, through='MateriaCarrera')

    def __str__(self):
        return self.nombre

    class Meta:
        unique_together = ('universidad', 'slug')


class MateriaCarrera(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    slug = models.SlugField(max_length=NOMBRE_MAX_LENGTH)
    optativa = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.nombre)
        if MateriaCarrera.objects.filter(
                slug=self.slug, carrera=self.carrera).exists():
            raise ValidationError(
                _('El slug de esta Materia es el '
                  'mismo que el de otra de la misma carrera.'))

    def get_absolute_url(self):
        return reverse('materia:materia', kwargs={'materia_carrera': self})

    class Meta:
        unique_together = (('carrera', 'materia'), ('carrera', 'slug'))
        ordering = ['nombre']
