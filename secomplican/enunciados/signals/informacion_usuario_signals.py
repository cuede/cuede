
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from enunciados.models import InformacionUsuario

@receiver(post_save, sender=User)
def crear_informacion_usuario(sender, instance, **kwargs):
    InformacionUsuario.objects.create(usuario=instance)


