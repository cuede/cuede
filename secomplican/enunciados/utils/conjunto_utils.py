from enunciados.models import Practica, Parcial, Final


def tipo_conjunto_a_url(conjunto):
    if isinstance(conjunto, Practica):
        return 'practicas'
    elif isinstance(conjunto, Parcial):
        if conjunto.recuperatorio:
            return 'recuperatorios'
        else:
            return 'parciales'
    elif isinstance(conjunto, Final):
        return 'finales'
    else:
        # No debería pasar nunca.
        return None


def tipo_de_conjunto(conjunto):
    """Devuelve el tipo del conjunto del conjunto pasado."""
    # Esto es horrible, pero no sé si hay otra forma de
    # chequear de qué subtipo es el conjunto.
    try:
        conjunto = conjunto.practica
        return 'practica'
    except Practica.DoesNotExist:
        try:
            conjunto = conjunto.parcial
            return 'parcial'
        except Parcial.DoesNotExist:
            try:
                conjunto = conjunto.final
                return 'final'
            except Final.DoesNotExist:
                # No debería pasar nunca.
                return None
