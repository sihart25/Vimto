from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter()
def to_int(value):
    if(value == ''):
        return 0
    else:
        return int(value)


@register.filter
def get_item_lng(dictionary, key):
    return dictionary.get(key).lng


@register.filter
def get_item_lat(dictionary, key):
    return dictionary.get(key).lat


@register.filter
def get_item_clr(dictionary, key):
    return dictionary.get(key).clr
