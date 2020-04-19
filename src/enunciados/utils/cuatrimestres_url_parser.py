from enunciados.models import ConjuntoDeEnunciadosConCuatrimestre

__CONVERSOR = {
    ConjuntoDeEnunciadosConCuatrimestre.PRIMERO: '1cuatri',
    ConjuntoDeEnunciadosConCuatrimestre.SEGUNDO: '2cuatri',
    ConjuntoDeEnunciadosConCuatrimestre.VERANO: 'verano',
}


def numero_a_url(numero):
    if numero in __CONVERSOR:
        return __CONVERSOR[numero]
    else:
        return None


def url_a_numero(cuatrimestre):
    """
    Devuelve el numero de cuatrimestre parseando el parámetro de una url.

    :returns: None si es que cuatrimestre no es uno entre '1cuatri', '2cuatri' o 'verano'
    """

    for numero, valor in __CONVERSOR.items():
        if valor == cuatrimestre:
            return numero
    return None
