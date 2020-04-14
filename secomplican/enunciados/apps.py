from django.apps import AppConfig


class EnunciadosConfig(AppConfig):
    name = 'enunciados'

    def ready(self):
        from enunciados.signals import informacion_usuario_signals
