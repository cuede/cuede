from django.db import migrations
from django.utils.text import slugify


MATERIAS = [
    'Calidad de Datos',
    'Reglas de Asociación y Patrones Secuenciales',
    'Tipos Comportamentales y Contratos',
    'Toma de Decisiones'
]


def agregar_materias(apps, schema_editor):
    """Agrega las materias optativas a la base de datos."""
    Carrera = apps.get_model('enunciados', 'Carrera')
    MateriaCarrera = apps.get_model('enunciados', 'MateriaCarrera')
    Materia = apps.get_model('enunciados', 'Materia')

    computacion = Carrera.objects.get(slug='computacion')
    for nombre_materia in MATERIAS:
        materia = Materia.objects.create()
        slug = slugify(nombre_materia)
        MateriaCarrera.objects.create(
            carrera=computacion, materia=materia, nombre=nombre_materia,
            slug=slug, optativa=True)


def sacar_materias(apps, schema_editor):
    Carrera = apps.get_model('enunciados', 'Carrera')
    MateriaCarrera = apps.get_model('enunciados', 'MateriaCarrera')
    Materia = apps.get_model('enunciados', 'Materia')

    computacion = Carrera.objects.get(slug='computacion')
    for nombre_materia in MATERIAS:
        slug = slugify(nombre_materia)
        MateriaCarrera.objects.get(carrera=computacion, slug=slug).materia.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('enunciados', '0027_informacion_usuario_eliminado'),
    ]

    operations = [
        migrations.RunPython(agregar_materias, sacar_materias),
    ]
