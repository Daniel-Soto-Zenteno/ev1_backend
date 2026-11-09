from django import template

register = template.Library()


@register.filter
def pesos_clp(value):
    return format(value, ',.0f').replace(',', '.')


@register.filter
def archivo_disponible(image):
    if not image:
        return False
    try:
        return image.storage.exists(image.name)
    except (OSError, ValueError):
        return False
