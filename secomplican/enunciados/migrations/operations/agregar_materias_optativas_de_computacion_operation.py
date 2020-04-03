from django.db.migrations.operations.base import Operation
from django.utils.text import slugify


class AgregarMateriasOptativasDeComputacionOperation(Operation):

    def __init__(self, materias):
        self.materias = materias

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        """Agrega las materias optativas a la base de datos."""
        Carrera = to_state.apps.get_model('enunciados', 'Carrera')
        MateriaCarrera = to_state.apps.get_model('enunciados', 'MateriaCarrera')
        Materia = to_state.apps.get_model('enunciados', 'Materia')

        computacion = Carrera.objects.get(slug='computacion')
        for nombre_materia in self.materias:
            materia = Materia()
            materia.save()
            slug = slugify(nombre_materia)
            MateriaCarrera.objects.create(
                carrera=computacion, materia=materia, nombre=nombre_materia,
                slug=slug, optativa=True)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        Carrera = to_state.apps.get_model('enunciados', 'Carrera')
        MateriaCarrera = to_state.apps.get_model('enunciados', 'MateriaCarrera')
        Materia = to_state.apps.get_model('enunciados', 'Materia')

        computacion = Carrera.objects.get(slug='computacion')
        for nombre_materia in self.materias:
            slug = slugify(nombre_materia)
            MateriaCarrera.objects.get(carrera=computacion, slug=slug).materia.delete()

    def describe(self):
        # This is used to describe what the operation does in console output.
        return "Agrega materias {} a la base de datos.".format(self.materias)

        from django.db import migrations
