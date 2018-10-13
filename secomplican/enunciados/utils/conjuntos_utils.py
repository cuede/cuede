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


def _ya_casteado(conjunto):
    """
    Decide si el conjunto pasado ya es una subclase de ConjuntoDeEnunciados.
    """
    return isinstance(conjunto, Practica) or \
        isinstance(conjunto, Parcial) or \
        isinstance(conjunto, Final)


def castear_a_subclase(conjunto):
    """
    'Castea' el conjunto a la subclase, porque en django los objetos conjunto
    son objetos separados de sus subclases.

    Por ejemplo, si un conjunto en realidad es una Practica, entonces
    devuelve la Practica de este conjunto.
    """
    if _ya_casteado(conjunto):
        casteado = conjunto
    else:
        tipo = tipo_conjunto(conjunto)
        if tipo == 'practica':
            casteado = conjunto.practica
        elif tipo == 'parcial':
            casteado = conjunto.parcial
        elif tipo == 'final':
            casteado = conjunto.final

    return casteado
