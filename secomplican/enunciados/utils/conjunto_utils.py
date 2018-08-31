from enunciados.models import Practica, Parcial, Final


def tipo_conjunto_a_url(conjunto):
    if isinstance(conjunto, Practica):
        return 'practica'
    elif isinstance(conjunto, Parcial):
        if conjunto.recuperatorio:
            return 'recuperatorio'
        else:
            return 'parcial'
    elif isinstance(conjunto, Final):
        return 'final'
    else:
        # No debería pasar nunca.
        return None


def tipo_de_conjunto(conjunto):
    """Devuelve el tipo del conjunto del conjunto pasado."""
    # Esto es horrible, pero no sé si hay otra forma de
    # chequear de qué subtipo es el conjunto.
    try:
        conjunto = conjunto.practica
    except Practica.DoesNotExist:
        try:
            conjunto = conjunto.parcial
        except Parcial.DoesNotExist:
            try:
                conjunto = conjunto.final
            except Final.DoesNotExist:
                # No debería pasar nunca.
                return None

    return tipo_conjunto_a_url(conjunto)

