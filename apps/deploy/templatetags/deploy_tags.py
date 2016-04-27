from django import template

register = template.Library()


@register.filter
def keyvalue(dict, key):
    return dict[key]


@register.filter
def div(value, arg):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int(value)
        arg = int(arg)
        if arg:
            return value / arg
    except Exception:
        pass
    return ''
