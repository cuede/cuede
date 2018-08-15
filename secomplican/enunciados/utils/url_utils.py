def add_query_params(url, **kwargs):
    """
    Agrega los query params al final de la url.

    La url tiene que no tener params todavía.
    """
    url += '?'
    for key, value in kwargs.items():
        url += '{key}={value}&'.format(key=key, value=value)
    return url
