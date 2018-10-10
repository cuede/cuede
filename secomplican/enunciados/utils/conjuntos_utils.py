from django.core.exceptions import ObjectDoesNotExist

from enunciados.models import Practica, Parcial, Final

TIPO_PRACTICA = 'practica'
TIPO_PARCIAL = 'parcial'
TIPO_FINAL = 'final'

__tipo_a_clase = {
    TIPO_PRACTICA: Practica,
    TIPO_PARCIAL: Parcial,
    TIPO_FINAL: Final,
}


def tipo_conjunto(conjunto):
    try:
        conjunto.practica
        tipo = TIPO_PRACTICA
    except ObjectDoesNotExist:
        try:
            conjunto.parcial
            tipo = TIPO_PARCIAL
        except ObjectDoesNotExist:
            try:
                conjunto.final
                tipo = TIPO_FINAL
            except ObjectDoesNotExist:
                raise ValueError('Tipo de conjunto no conocido')

    return tipo


def tipo_a_clase(tipo):
    """
    Convierte un string de tipo devuelto por tipo_conjunto
    a la clase correspondiente.
    """
    return __tipo_a_clase[tipo]
