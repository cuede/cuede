from django.test import TestCase
from django.contrib.auth.models import User
from enunciados.models import InformacionUsuario


class InformacionUsuarioTests(TestCase):
    def test_crear_un_usuario_deberia_crear_informacion_con_cero_puntos(self):
        usuario = User.objects.create(username='user', password='pass')
        info = InformacionUsuario.objects.get(usuario__username='user')

        self.assertEquals(info.usuario, usuario)
        self.assertEquals(info.puntos, 0)

    def test_no_se_pueden_poner_puntos_negativos(self):
        usuario = User.objects.create(username='user', password='pass')
        info = InformacionUsuario.objects.get(usuario=usuario)
        info.puntos -= 5

        with self.assertRaises(Exception):
            info.save()

    def test_se_puede_actualizar_un_usuario(self):
        """No se debería crear dos veces la InformacionUsuario"""
        usuario = User.objects.create(username='user', password='pass')
        usuario.set_password('pass')
        usuario.save()
        info = InformacionUsuario.objects.get(usuario=usuario)

        self.assertEquals(info.usuario, usuario)
