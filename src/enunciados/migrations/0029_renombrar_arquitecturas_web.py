from django.db import migrations
from django.utils.text import slugify

ORIGINAL = 'Arquitecturas Web'
NUEVO = 'Arquitecturas de Aplicaciones Web'

def cambiar_nombre(apps, original, nuevo):
    MateriaCarrera = apps.get_model('enunciados', 'MateriaCarrera')
    materia = MateriaCarrera.objects.get(nombre=original)
    materia.nombre = nuevo
    materia.save()

def para_adelante(apps, schema_editor):
    cambiar_nombre(apps, ORIGINAL, NUEVO)

def para_atras(apps, schema_editor):
    cambiar_nombre(apps, NUEVO, ORIGINAL)

class Migration(migrations.Migration):

    dependencies = [
        ('enunciados', '0028_materias_optativas_cuatri1_2020'),
    ]

    operations = [
        migrations.RunPython(para_adelante, para_atras)
    ]
