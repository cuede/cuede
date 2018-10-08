from django.core.exceptions import ObjectDoesNotExist


def tipo_conjunto(conjunto):
    try:
        conjunto.practica
        tipo = 'practica'
    except ObjectDoesNotExist:
        try:
            conjunto.parcial
            tipo = 'parcial'
        except ObjectDoesNotExist:
            try:
                conjunto.final
                tipo = 'final'
            except ObjectDoesNotExist:
                raise ValueError('Tipo de conjunto no conocido')

    return tipo
