def truncar(texto, max_caracteres=32):
    """
    Trunca el texto para que tenga maximo max_caracteres caracteres,
    contando los tres puntos que se agregan al final si es que el texto tiene mas de
    max_caracteres caracteres.
    """
    return (texto[:max_caracteres - 3] + '...') if len(texto) > max_caracteres + 3 else texto
