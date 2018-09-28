from enunciados.models import Practica, Parcial, Final


def tipo_conjunto(conjunto):
    try:
        conjunto.practica
        tipo = 'practica'
    except Practica.DoesNotExist:
        try:
            conjunto.parcial
            tipo = 'parcial'
        except Parcial.DoesNotExist:
            try:
                conjunto.final
                tipo = 'final'
            except Final.DoesNotExist:
                raise ValueError('Tipo de conjunto no conocido')

    return tipo
