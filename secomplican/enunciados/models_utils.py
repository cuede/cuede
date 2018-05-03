def tiene_practica_con_materia(cuatrimestre, materia):
    """
    Define si el Cuatrimestre tiene alguna práctica que pretenezca a la materia.

    :param materia: Nombre de la materia.
    """
    return any(practica.materia.nombre == materia for practica in cuatrimestre.practica_set.all())
