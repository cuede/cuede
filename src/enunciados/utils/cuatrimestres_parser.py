# Convierte un número de cuatrimestre a un texto de cuatrimestre, por ejemplo, "Primer cuatrimestre".
from django.utils.translation import gettext as _

from enunciados.models import ConjuntoDeEnunciadosConCuatrimestre


def numero_a_texto(numero):
    return ConjuntoDeEnunciadosConCuatrimestre.TEXTOS_CUATRIMESTRE.get(numero)