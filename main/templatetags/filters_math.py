from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    """{{ value|sub:"arg" }}"""
    arg = int(arg)
    return value - arg
