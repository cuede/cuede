from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Materia)
admin.site.register(Practica)
admin.site.register(Parcial)
admin.site.register(Final)
admin.site.register(Enunciado)
admin.site.register(VersionTextoEnunciado)
admin.site.register(VersionTextoSolucion)