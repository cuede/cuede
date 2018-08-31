import re


from enunciados.utils import cuatrimestres_url_parser, conjunto_utils
from enunciados.models import Practica, Parcial, Final

class ConjuntoConverter:
    regex_materia = r'([-\w]+)/'
    regex_cuatrimestre = r'(verano|1cuatri|2cuatri)/'
    regex_anio = r'([0-9]{4})/'
    regex_mes = r'([0-9]{2})/'
    regex_dia = r'([0-9]{2})'
    regex_numero = r'([0-9]+)'
    regex_practica = r'(practicas)/' + \
        regex_anio + regex_cuatrimestre + regex_numero
    regex_parcial = r'(parciales)/' + \
        regex_anio + regex_cuatrimestre + regex_numero
    regex_recuperatorio = r'(recuperatorios)/' + \
        regex_anio + regex_cuatrimestre + regex_numero
    regex_final = r'(finales)/' + \
        regex_anio + regex_mes + regex_dia
    regex = regex_materia + '(' + regex_practica + '|' + regex_parcial + '|' + \
        regex_recuperatorio + '|' + regex_final + ')'

    def to_python(self, value):
        import pdb; pdb.set_trace()
        match = re.match(self.regex, value)
        slug_materia = match.group(1)
        get_kwargs = {
            'materia__slug': slug_materia,
        }
        anio = int(match.group(4))
        conjunto = match.group(3)
        if conjunto == 'finales':
            mes = int(match.group('mes'))
            dia = int(match.group('dia'))
            model = Final
            get_kwargs.update({
                'fecha__year': anio,
                'fecha__month': mes,
                'fecha__day': dia,
            })
        else:
            cuatrimestre = cuatrimestres_url_parser.url_a_numero(
                match.group(5)
            )
            numero = match.group(6)
            get_kwargs.update({
                'anio': anio,
                'cuatrimestre': cuatrimestre,
                'numero': numero,
            })

            if conjunto == 'practicas':
                anio = int(match.group(4))
                url_cuatrimestre = match.group(5)
                numero = match.group(6)
                model = Practica
            elif conjunto == 'parciales':
                model = Parcial
            elif conjunto == 'recuperatorios':
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
        string = '{materia}/{conjunto}/'.format(
            materia=value.materia.slug, conjunto=url_conjunto)
        string += '{anio:04d}/'
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
