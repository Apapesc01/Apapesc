from django import template

register = template.Library()

STATUS_MAP = {
    'associado_lista_ativo': ('Ativo', 'badge-green'),
    'associado_lista_aposentado': ('Aposentado', 'badge-blue'),
    'candidato': ('Candidato', 'badge-orange'),
    'cliente_especial': ('Cliente Especial', 'badge-purple'),
    'extra_associado': ('Extra', 'badge-gray'),
    'desassociado': ('Desassociado', 'badge-red'),
}

@register.filter
def status_resumido(value):
    return STATUS_MAP.get(value, ('Indefinido', 'badge-gray'))[0]

@register.filter
def status_cor(value):
    return STATUS_MAP.get(value, ('Indefinido', 'badge-gray'))[1]
