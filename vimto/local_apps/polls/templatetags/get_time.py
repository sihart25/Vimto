from django.template.defaulttags import register
import datetime 

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

