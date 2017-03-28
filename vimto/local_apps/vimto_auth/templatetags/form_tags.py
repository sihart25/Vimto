""" Template tags for forms. """
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def replace_underscore(value):
    return value.replace('_', ' ')


@register.filter
def form_field_value(form, field):
    ''' Return the value of a form field. '''
    try:
        return form.data.get(field, "")
    except:
        return ""
