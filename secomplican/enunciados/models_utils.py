def parciales_ordenados(materia):
    """Devuelve todos los parciales de la materia seleccionada ordenados de ultimo cuatrimestre a primero."""
    return materia.conjuntodeenunciados_set \
        .filter(parcial__isnull=False) \
        .order_by('-cuatrimestre__anio', '-cuatrimestre__cuatrimestre')


def ultimas_practicas_ordenadas(materia):
    """
    Devuelve todas las practicas de la materia que esten en el ultimo cuatrimestre en el que
    hay practicas para la materia.
    :param materia:
    :return:
    """
    practicas_descendientes = materia.conjuntodeenunciados_set \
        .filter(practica__isnull=False) \
        .order_by('-cuatrimestre__anio', '-cuatrimestre__cuatrimestre')
    if practicas_descendientes:
        ultimo_cuatrimestre = practicas_descendientes[0].cuatrimestre
        practicas_descendientes = practicas_descendientes.filter(cuatrimestre=ultimo_cuatrimestre)
    return practicas_descendientes