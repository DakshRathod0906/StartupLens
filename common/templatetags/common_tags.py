from django import template

register = template.Library()

@register.filter(name='split')
def split_filter(value, delimiter=','):
    """Split a string by delimiter."""
    if not isinstance(value, str):
        return []
    return value.split(delimiter)

@register.filter(name='replace_underscores')
def replace_underscores(value):
    """Replace all underscores with spaces."""
    if not isinstance(value, str):
        return str(value)
    return value.replace("_", " ")

