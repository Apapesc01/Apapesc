import re
from django import forms

def validate_and_format_cpf(value):
    cpf_numeros = re.sub(r'\D', '', value)
    if len(cpf_numeros) != 11:
        raise forms.ValidationError('CPF inválido. Deve conter 11 números.')
    return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"

def validate_and_format_cnpj(value):
    cnpj_numeros = re.sub(r'\D', '', value)
    if len(cnpj_numeros) != 14:
        raise forms.ValidationError('CNPJ inválido. Deve conter 14 números.')
    return f"{cnpj_numeros[:2]}.{cnpj_numeros[2:5]}.{cnpj_numeros[5:8]}/{cnpj_numeros[8:12]}-{cnpj_numeros[12:]}"

def validate_and_format_celular(value):
    if not value:
        return value  # Se o campo não for obrigatório

    celular_numeros = re.sub(r'\D', '', value)
    if len(celular_numeros) not in [10, 11]:
        raise forms.ValidationError('Número de celular inválido. Informe 11 dígitos. (00) 00000-0000')
    
    ddd = celular_numeros[:2]
    numero = celular_numeros[2:]
    if len(numero) == 9:
        return f"({ddd}){numero[:5]}-{numero[5:]}"
    else:
        return f"({ddd}){numero[:4]}-{numero[4:]}"
    


def validate_and_format_cep(value):
    if not value:
        return value  # Retorna vazio ou None se for opcional

    cep_numeros = re.sub(r'\D', '', value)
    if len(cep_numeros) != 8:
        raise forms.ValidationError('CEP inválido. Deve conter exatamente 8 números.')

    return f"{cep_numeros[:5]}-{cep_numeros[5:]}"
