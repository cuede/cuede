from enunciados.models import Practica, Parcial, Final

def tipo_de_conjunto(conjunto):
    """Devuelve el tipo del conjunto del conjunto pasado."""
    # Esto es horrible, pero no sé si hay otra forma de
    # chequear de qué subtipo es el conjunto.
    try:
        practica = conjunto.practica
        return 'practica'
    except Practica.DoesNotExist:
        try:
            parcial = conjunto.parcial
            return 'parcial'
        except Parcial.DoesNotExist:
            try:
                final = conjunto.final
                return 'final'
            except Final.DoesNotExist:
                # No debería pasar nunca.
                return None

