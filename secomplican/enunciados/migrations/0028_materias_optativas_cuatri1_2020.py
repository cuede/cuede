from django.db import migrations
from django.utils.text import slugify
from enunciados.migrations.operations.agregar_materias_optativas_de_computacion_operation import AgregarMateriasOptativasDeComputacionOperation


MATERIAS = [
    'Calidad de Datos',
    'Reglas de Asociación y Patrones Secuenciales',
    'Tipos Comportamentales y Contratos',
    'Toma de Decisiones'
]

class Migration(migrations.Migration):

    dependencies = [
        ('enunciados', '0027_informacion_usuario_eliminado'),
    ]

    operations = [
        AgregarMateriasOptativasDeComputacionOperation(MATERIAS),
    ]
