from enunciados.models import ConjuntoDeEnunciadosConCuatrimestre


def __castear_a_parciales(conjuntos_de_enunciados):
    return [conjunto.parcial for conjunto in conjuntos_de_enunciados]


def __castear_a_practicas(conjuntos_de_enunciados):
    return [conjunto.practica for conjunto in conjuntos_de_enunciados]


def __castear_a_finales(conjuntos_de_enunciados):
    return [conjunto.final for conjunto in conjuntos_de_enunciados]


def __separar_por_numero(parciales):
    """Devuelve un conjunto de conjuntos de parciales, separados por numero."""
    separados = {}
    for parcial in parciales:
        numero = parcial.numero
        if numero in separados:
            separados[numero].append(parcial)
        else:
            separados[numero] = [parcial]

    return separados


def __comparador_numero_cuatrimestre(numero_cuatrimestre):
    """
    Devuelve un número que se puede usar para comparar entre
    números de cuatrimestre de anterior a posterior.
    """
    if numero_cuatrimestre == ConjuntoDeEnunciadosConCuatrimestre.VERANO:
        return 1
    elif numero_cuatrimestre == ConjuntoDeEnunciadosConCuatrimestre.PRIMERO:
        return 2
    else:
        return 3


def __comparador_cuatrimestre(conjunto):
    """
    Devuelve un número que se puede usar para comparar entre conjuntos con cuatrimestre
    para determinar cuál es más reciente.
    """
    comparador_numero = __comparador_numero_cuatrimestre(conjunto.cuatrimestre)
    string_comparador = '{anio}{numero}' \
        .format(anio=conjunto.anio, numero=comparador_numero)
    return int(string_comparador)


def __comparador_practica(practica):
    """
    Devuelve un número que se puede usar para comparar entre prácticas.
    """
    # Asumimos que el número de práctica no va a superar 99
    return __comparador_cuatrimestre(practica) * 100 + (100 - practica.numero)


def __comparador_parcial(parcial):
    """
    Devuelve un número que se puede usar para comparar entre parciales.
    """
    comparador_recuperatorio = 1 if parcial.recuperatorio else 0
    string_comparador = '{}{}'.format(__comparador_cuatrimestre(parcial), comparador_recuperatorio)
    return int(string_comparador)


def __ordenar_practicas(practicas):
    """
    Ordena las prácticas de mayor a menor en cuatrimestre y de menor a
    mayor en número.
    """
    return sorted(practicas, key=__comparador_practica, reverse=True)


def __ordenar_parciales(parciales):
    """
    Ordena los parciales de más reciente a menos reciente.

    Pone a los recuperatorios antes que los parciales.
    """
    return sorted(parciales, key=__comparador_parcial, reverse=True)


def parciales_de_materia(materia):
    """
    Devuelve una lista de los parciales que pertenecen a la materia.

    :param materia: No puede ser None.
    """
    if not materia:
        raise ValueError('Materia no debería ser None.')

    conjuntos = materia.conjuntodeenunciados_set.filter(parcial__isnull=False)
    return __castear_a_parciales(conjuntos)


def parciales_de_materia_ordenados(materia):
    """
    Devuelve una lista de conjuntos de parciales,
    cada conjunto ordenado por cuatrimestre.

    :param materia: No puede ser None.
    """
    parciales = parciales_de_materia(materia)
    parciales_por_numero = __separar_por_numero(parciales)
    for numero, parciales_de_numero in parciales_por_numero.items():
        parciales_por_numero[numero] = __ordenar_parciales(parciales_de_numero)
    return parciales_por_numero


def practicas_de_materia(materia):
    """
    Devuelve una lista de los parciales que pertenecen a la materia.

    :param materia: No puede ser None.
    """
    if not materia:
        raise ValueError('Materia no debería ser None.')

    conjuntos = materia.conjuntodeenunciados_set.filter(practica__isnull=False)
    return __castear_a_practicas(conjuntos)


def _mismo_momento(conjunto1, conjunto2):
    """Determina si dos conjuntos con cuatrimestre ocurrieron en el mismo cuatrimestre del mismo año."""
    return conjunto1.cuatrimestre == conjunto2.cuatrimestre and conjunto1.anio == conjunto2.anio


def ultimas_practicas_ordenadas(materia):
    """
    Devuelve todas las prácticas de la materia que estén en el último cuatrimestre en el que
    hay prácticas para la materia.
    """
    practicas = practicas_de_materia(materia)
    practicas_ordenadas = __ordenar_practicas(practicas)
    if practicas_ordenadas:
        ultima_practica = practicas_ordenadas[0]
        practicas_ordenadas = list(filter(lambda p: _mismo_momento(ultima_practica, p), practicas_ordenadas))

    return practicas_ordenadas


def finales_de_materia(materia):
    """
    Devuelve una lista de los finales que pertenecen a la materia.

    :param materia: No puede ser None.
    """
    if not materia:
        raise ValueError('Materia no debería ser None.')

    conjuntos = materia.conjuntodeenunciados_set.filter(final__isnull=False)
    return __castear_a_finales(conjuntos)


def finales_de_materia_ordenados(materia):
    """
    Devuelve una lista de finales ordenados por fecha de último a primero.

    :param materia: No puede ser None.
    """
    finales = finales_de_materia(materia)
    return sorted(finales, key=lambda f: f.fecha, reverse=True)
