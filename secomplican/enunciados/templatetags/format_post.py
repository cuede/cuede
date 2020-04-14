import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape, linebreaks
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def format_post(texto, autoescape=True):
    """Replaces matches of code surrounded by ``` ``` with pre tags."""
    if autoescape:
        texto = conditional_escape(texto)

    partes = texto.split('```')
    for i in range(0, len(partes), 2):
        partes[i] = format_text_part(partes[i])

    for i in range(1, len(partes), 2):
        if len(partes) > i + 1:
            partes[i] = format_code_part(partes[i])
        else:
            partes[i] = linebreaks('```' + partes[i])

    new_text = ''.join(partes)
    return mark_safe(new_text)


def format_text_part(part):
    part = part.strip()
    if part:
        part = linebreaks(part)
    return part

def format_code_part(part):
    return '<pre>{}</pre>'.format(part)
