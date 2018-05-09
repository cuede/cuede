from django.db import models

class Materia(models.Model):
    nombre = models.CharField(max_length=1023)

    def __str__(self):
        return self.nombre


class Cuatrimestre(models.Model):
    """
    Representa la etapa de un año: 1er cuatrimestre, 2do cuatrimestre, o verano.
    """
    anio = models.IntegerField()

    PRIMERO = 1
    SEGUNDO = 2
    VERANO = 3
    NUMERO_CHOICES = (
        (PRIMERO, 'Primer Cuatrimestre'),
        (SEGUNDO, 'Segundo Cuatrimestre'),
        (VERANO, 'Verano')
    )

    numero = models.IntegerField(choices=NUMERO_CHOICES)

    def __str_cuatrimestre(self):
        if self.numero == self.PRIMERO:
            return 'Primer Cuatrimestre'
        elif self.numero == self.SEGUNDO:
            return 'Segundo Cuatrimestre'
        else:
            return 'Verano'

    def __str__(self):
        return '{} del {}'.format(self.__str_cuatrimestre(), self.anio)

    class Meta:
        unique_together = ('anio', 'numero')


class ConjuntoDeEnunciados(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)


class ConjuntoDeEnunciadosConCuatrimestre(ConjuntoDeEnunciados):
    cuatrimestre = models.ForeignKey(Cuatrimestre, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Practica(ConjuntoDeEnunciadosConCuatrimestre):
    numero = models.IntegerField()
    titulo = models.CharField(max_length=1023, default='')

    def __str__(self):
        return '{} - Practica {} del {}'.format(self.materia, self.numero, self.cuatrimestre)


class Parcial(ConjuntoDeEnunciadosConCuatrimestre):
    numero = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    recuperatorio = models.BooleanField(default=False)

    def __str__(self):
        nombre = 'Parcial'
        if self.recuperatorio:
            nombre = 'Recuperatorio'
        return '{} - {} {} del {}'.format(self.materia, self.ordinal()['singular'], nombre, self.cuatrimestre)

    def ordinal(self):
        """
        Devuelve el adjetivo ordinal correspondiente al número de este parcial,
        tanto en singular como en plural.
        """
        # Asumimos que no hay mas de cuatro parciales. Deberíamos quizá usar una library que te provea los ordinales.
        ordinales = [
            {'singular': 'Primer', 'plural': 'Primeros'},
            {'singular': 'Segundo', 'plural': 'Segundos'},
            {'singular': 'Tercer', 'plural': 'Terceros'},
            {'singular': 'Cuarto', 'plural': 'Cuartos'},
        ]
        return ordinales[self.numero - 1]


class Final(ConjuntoDeEnunciados):
    fecha = models.DateField()

    def __str__(self):
        return '{} - Final del {}'.format(self.materia, self.fecha)


class VersionesManager(models.Manager):
    def ultima(self):
        queryset = self.get_queryset()
        if queryset:
            return queryset.all()[0]
        else:
            return ''


class Enunciado(models.Model):
    conjunto = models.ForeignKey(ConjuntoDeEnunciados, on_delete=models.CASCADE)
    # El numero de enunciado en el conjunto de enunciados.
    numero = models.IntegerField()

    def __str__(self):
        return 'Enunciado {}'.format(self.numero)

    def get_absolute_url(self):
        from django.urls import reverse
        from . import cuatrimestres_url_parser
        kwargs = {
            'materia': self.conjunto.materia.nombre,
            'numero': self.numero,
        }

        # Esto es horrible, pero no sé si hay otra forma de chequear de qué subtipo es el conjunto.
        try:
            parcial = self.conjunto.parcial
            kwargs['conjunto_de_enunciados'] = parcial.numero
            kwargs['anio'] = parcial.cuatrimestre.anio
            kwargs['cuatrimestre'] = cuatrimestres_url_parser.numero_a_url(parcial.cuatrimestre.numero)
            if parcial.recuperatorio:
                url = 'enunciado_recuperatorio'
            else:
                url = 'enunciado_parcial'
        except Parcial.DoesNotExist:
            try:
                practica = self.conjunto.practica
                kwargs['conjunto_de_enunciados'] = practica.numero
                kwargs['anio'] = practica.cuatrimestre.anio
                kwargs['cuatrimestre'] = cuatrimestres_url_parser.numero_a_url(practica.cuatrimestre.numero)
                url = 'enunciado_practica'
            except Practica.DoesNotExist:
                try:
                    final = self.conjunto.final
                    kwargs['anio'] = final.fecha.year
                    kwargs['mes'] = final.fecha.month
                    kwargs['dia'] = final.fecha.day
                    url = 'enunciado_final'
                except Final.DoesNotExist:
                    raise Exception('El Enunciado no tiene un tipo de ConjuntoDeEnunciados conocido.')

        return reverse(url, kwargs=kwargs)

    class Meta:
        ordering = ['numero']
        # No puede haber dos ejercicios con el mismo número en el mismo conjunto.
        unique_together = ('numero', 'conjunto')


class VersionTexto(models.Model):
    tiempo = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()
    versiones = VersionesManager()

    def __str__(self):
        return self.texto

    class Meta:
        # Ordenamos del más reciente al más viejo.
        ordering = ['-tiempo']
        abstract = True


class VersionTextoEnunciado(VersionTexto):
    enunciado = models.ForeignKey(Enunciado, on_delete=models.CASCADE, related_name='versiones')


class Solucion(models.Model):
    enunciado = models.ForeignKey(Enunciado, on_delete=models.CASCADE)


class VersionTextoSolucion(VersionTexto):
    solucion = models.ForeignKey(Solucion, on_delete=models.CASCADE, related_name='versiones')
