def add_query_params(url, **kwargs):
    """
    Agrega los query params al final de la url.

    La url tiene que no tener params todavía.
    """
    def parametrizar(tupla):
        return '{key}={value}'.format(key=tupla[0], value=tupla[1])

    parametros = map(parametrizar, kwargs.items())
    parametros_unidos = '&'.join(parametros)
    if parametros_unidos:
        url += '?' + parametros_unidos
    return url
