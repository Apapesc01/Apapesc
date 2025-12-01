from django import template

register = template.Library()

@register.filter
def moeda_br(value):
    try:
        value = float(value)
    except:
        return value

    return f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
