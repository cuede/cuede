from django.test import TestCase
from django.contrib.auth import get_user_model

from enunciados.models import Materia, Practica, Enunciado


def agregar_enunciado(conjunto, numero):
    enunciado = Enunciado(conjunto=conjunto, numero=numero, texto='')
    enunciado.save()
    return enunciado


class VersionTextoEnunciadoTests(TestCase):
    def setUp(self):
        materia = Materia()
        materia.save()
        conjunto = Practica(
            materia=materia, anio=2018, cuatrimestre=1, numero=1)
        conjunto.save()
        self.enunciado = Enunciado(conjunto=conjunto, numero=1)
        self.enunciado.save()

    def test_ordenamiento(self):
        """Deberían estar ordenados por tiempo de más reciente a menos reciente."""
        usuario = get_user_model().objects.create_user(username='user', password='pass')
        self.enunciado.versiones.create(texto='hola', autor=usuario)
        self.enunciado.versiones.create(texto='chau', autor=usuario)
        self.enunciado.versiones.create(texto='que tal', autor=usuario)
        self.enunciado.versiones.create(texto='foobar', autor=usuario)

        versiones = self.enunciado.versiones.all()
        for index, version in enumerate(versiones):
            if index < len(versiones) - 1:
                self.assertGreaterEqual(
                    version.tiempo, versiones[index + 1].tiempo)
