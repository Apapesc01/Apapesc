from django import forms
from .models import ServicoModel, EntradaFinanceiraModel, PagamentoEntrada
from django.forms import DateInput
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db.models import Sum
from core.choices import TIPO_SERVICO, STATUS_ASSESSORIA_PROCESSO, STATUS_EMISSAO_DOC, STATUS_CONSULTORIA  # ou apenas os que você precisa


class ServicoForm(forms.ModelForm):
    class Meta:
        model = ServicoModel
        fields = [
            'natureza_servico', 'tipo_servico', 'associacao', 'reparticao',
            'valor', 'status_servico', 'content', 'associado'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 50, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['associacao'].required = True
        self.fields['reparticao'].required = True

        self.fields['natureza_servico'].widget.attrs.update({'class': 'js-natureza-servico'})
        self.fields['tipo_servico'].widget.attrs.update({'class': 'js-tipo-servico'})
        self.fields['tipo_servico'].widget.attrs.update({'class': 'js-tipo-servico'})
        self.fields['status_servico'].widget.attrs.update({'class': 'js-status-servico'})

                    
                
class EntradaFinanceiraForm(forms.ModelForm):
    class Meta:
        model = EntradaFinanceiraModel
        fields = [
            'servico',
            'forma_pagamento',
            'parcelamento',
            'valor',
            'pago',
            'valor_pagamento',
        ]
        widgets = {
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'parcelamento': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['forma_pagamento'].required = True
        self.fields['parcelamento'].required = True
        self.fields['valor'].required = True

# Registrar - Pagamento Form
class PagamentoEntradaForm(forms.ModelForm):
    class Meta:
        model = PagamentoEntrada
        fields = [
            'valor_pago',
            'data_pagamento',
            'comprovante_up',
        ]
        widgets = {
            'data_pagamento': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.servico = None
        if self.instance and self.instance.pk:
            self.servico = self.instance.servico
        elif 'servico' in self.initial:
            self.servico = self.initial['servico']

    def clean_valor_pago(self):
        valor_pago = self.cleaned_data.get('valor_pago') or Decimal('0.00')
        servico = self.servico
        if not servico:
            return valor_pago

        entrada = getattr(servico, 'entrada_servico', None)
        if not entrada:
            return valor_pago

        # Soma todos os pagamentos já realizados, exceto este (caso edição)
        pagamentos = servico.pagamentos.all()
        if self.instance.pk:
            pagamentos = pagamentos.exclude(pk=self.instance.pk)
        total_ja_pago = pagamentos.aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')

        # Quanto falta pagar
        valor_restante = entrada.valor - total_ja_pago

        if valor_pago > valor_restante:
            raise ValidationError(f'O valor máximo permitido é R$ {valor_restante:.2f}.')

        return valor_pago
    


class ServicoSearchForm(forms.Form):
    associado_nome = forms.CharField(label='Associado', required=False)
    tipo_servico = forms.ChoiceField(
        label='Tipo de Serviço',
        choices=[('', '---')] + TIPO_SERVICO,
        required=False
    )
    status_servico = forms.ChoiceField(
        label='Status',
        choices=[('', '---')] 
                 + STATUS_ASSESSORIA_PROCESSO 
                 + STATUS_EMISSAO_DOC 
                 + STATUS_CONSULTORIA,
        required=False
    )