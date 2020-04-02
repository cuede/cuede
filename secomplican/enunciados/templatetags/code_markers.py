import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def code_markers(texto, autoescape=True):
    """Replaces matches of code surrounded by ``` ``` with pre tags."""
    if autoescape:
        texto = conditional_escape(texto)
    new_text = re.sub(r'```(.*?)```', r'<pre>\1</pre>', texto, flags=re.DOTALL)
    return mark_safe(new_text)
