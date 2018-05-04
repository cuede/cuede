def parciales_ordenados(materia):
    """Devuelve todos los parciales de la materia seleccionada ordenados de ultimo cuatrimestre a primero."""
    return materia.conjuntodeenunciados_set \
        .filter(parcial__isnull=False) \
        .order_by('-cuatrimestre__anio', '-cuatrimestre__cuatrimestre')
