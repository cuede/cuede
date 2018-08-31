import re


from enunciados.utils import cuatrimestres_url_parser, conjunto_utils
from enunciados.models import Practica, Parcial, Final

class ConjuntoConverter:
    regex_materia = r'(?P<materia>[-\w]+)/'
    regex_cuatrimestre = r'(?P<cuatrimestre>verano|1cuatri|2cuatri)/'
    regex_anio = r'(?P<anio>[0-9]{4})/'
    regex_mes = r'(?P<mes>[0-9]{2})/'
    regex_dia = r'(?P<dia>[0-9]{2})/'
    regex_numero = r'(?P<numero>[0-9]+)/'
    regex_practica = r'(?P<conjunto>practica)/' + \
        regex_anio + regex_cuatrimestre + regex_numero
    regex_parcial = r'(?P<conjunto>parcial)/' + \
        regex_anio + regex_cuatrimestre + regex_numero
    regex_recuperatorio = r'(?P<conjunto>recuperatorio)/' + \
        regex_anio + regex_cuatrimestre + regex_numero
    regex_final = r'(?P<conjunto>recuperatorio)/' + \
        regex_anio + regex_mes + regex_dia
    regex = regex_materia + '(' + regex_practica + '|' + regex_parcial + '|' + \
        regex_recuperatorio + '|' + regex_final + ')'

    def to_python(self, value):
        match = re.match(self.regex, value)
        slug_materia = match.group('materia')
        get_kwargs = {
            'materia__slug': slug_materia,
        }
        anio = int(match.group('anio'))
        conjunto = match.group('conjunto')
        if conjunto == 'final':
            mes = int(match.group('mes'))
            dia = int(match.group('dia'))
            model = Final
            get_kwargs += {
                'fecha__year': anio,
                'fecha__month': mes,
                'fecha__day': dia,
            }
        else:
            cuatrimestre = cuatrimestres_url_parser.url_a_numero(
                match.group('cuatrimestre')
            )
            get_kwargs += {
                'anio': anio,
                'cuatrimestre': cuatrimestre,
            }

            if conjunto == 'practica':
                model = Practica
            elif conjunto == 'parcial':
                model = Parcial
            elif conjunto == 'recuperatorio':
                model = Parcial
                get_kwargs['recuperatorio'] = True
            else:
                raise ValueError

        try:
            return model.objects.get(**get_kwargs)
        except:
            raise ValueError

    def to_url(self, value):
        """El value debería ser una Practica, un Parcial, o un Final."""
        url_conjunto = conjunto_utils.tipo_conjunto_a_url(value)
        string = '{materia}/{conjunto}/{anio:04d}/'.format(
            materia=value.materia, conjunto=url_conjunto)
        if isinstance(value, Final):
            string += '{mes:02d}/{dia:02d}/'
            url = string.format(
                anio=value.fecha.year,
                mes=value.fecha.month,
                dia=value.fecha.day,
            )
        else:
            cuatrimestre = cuatrimestres_url_parser.numero_a_url(
                value.cuatrimestre)
            string += '{cuatrimestre}/{numero}/'
            url = string.format(
                anio=value.anio,
                cuatrimestre=cuatrimestre,
                numero=value.numero,
            )

        return url
