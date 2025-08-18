# app_associados/templatetags/status_tags.py
from django import template

register = template.Library()

@register.filter
def status_badge_class(status_value: str) -> str:
    """
    Mapeia o status do associado para a classe CSS do badge.
    """
    mapping = {
        'associado_lista_ativo':      'status-ativo',
        'associado_lista_aposentado': 'status-aposentado',
        'candidato':                   'status-candidato',
        'cliente_especial':            'status-especial',
        'extra_associado':             'status-extra',
        'desassociado':                'status-desassociado',
    }
    return mapping.get(status_value, 'status-candidato')  # fallback suave
