from django import template

register = template.Library()


@register.simple_tag
def list(*args):
    return args
