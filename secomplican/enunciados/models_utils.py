def tiene_practica_con_materia(etapa, materia):
    """
    Define si la Etapa tiene alguna práctica que pretenezca a la materia.

    :param materia: Nombre de la materia.
    """
    return any(practica.materia.nombre == materia for practica in etapa.practica_set.all())
