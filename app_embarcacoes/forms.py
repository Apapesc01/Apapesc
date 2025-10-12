from django import forms
from .models import EmbarcacoesModel

class EmbarcacaoForm(forms.ModelForm):
    class Meta:
        model = EmbarcacoesModel
        exclude = ('data_atualizacao',)
        widgets = {
            'validade_tie': forms.DateInput(attrs={'type': 'date'}),
            'data_emissao': forms.DateInput(attrs={'type': 'date'}),
            'seguro_dpem_data_vencimento': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'documento_tie': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'documento_licenca': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # opcional: pré-definir o proprietário e travar o campo
        proprietario_initial = kwargs.pop('proprietario', None)
        super().__init__(*args, **kwargs)

        # IDs úteis para JS
        self.fields['proprietario'].widget.attrs.update({'id': 'id_proprietario'})
        self.fields['tipo_embarcacao'].widget.attrs.update({'id': 'id_tipo_embarcacao'})
        self.fields['tipo_propulsao'].widget.attrs.update({'id': 'id_tipo_propulsao'})
        self.fields['combustivel'].widget.attrs.update({'id': 'id_combustivel'})
        self.fields['porte'].widget.attrs.update({'id': 'id_porte'})

        # Preenche datas no formato yyyy-mm-dd em edição
        date_fields = ('validade_tie', 'data_emissao', 'seguro_dpem_data_vencimento')
        if self.instance and self.instance.pk:
            for fname in date_fields:
                val = getattr(self.instance, fname, None)
                if val:
                    self.fields[fname].widget.attrs['value'] = val.strftime('%Y-%m-%d')

        if proprietario_initial:
            self.fields['proprietario'].initial = proprietario_initial
            self.fields['proprietario'].disabled = True

    # ---- Validações de consistência ----
    def clean(self):
        cleaned = super().clean()
        validade_tie = cleaned.get('validade_tie')
        data_emissao = cleaned.get('data_emissao')

        if validade_tie and data_emissao and validade_tie < data_emissao:
            self.add_error('validade_tie', 'A validade da TIE não pode ser anterior à data de emissão.')

        # Regras do DPEM: se “sim”, exigir número e vencimento
        seguro_dpem = cleaned.get('seguro_dpem')
        if seguro_dpem == 'sim':
            if not cleaned.get('seguro_dpem_numero'):
                self.add_error('seguro_dpem_numero', 'Informe o número da apólice do DPEM.')
            if not cleaned.get('seguro_dpem_data_vencimento'):
                self.add_error('seguro_dpem_data_vencimento', 'Informe a data de vencimento do DPEM.')
        return cleaned

    # Normalizações simples (opcional)
    def clean_nome_embarcacao(self):
        nome = (self.cleaned_data.get('nome_embarcacao') or '').strip()
        return ' '.join(nome.split())

    def clean_inscricao_embarcacao(self):
        ins = (self.cleaned_data.get('inscricao_embarcacao') or '').strip().upper()
        return ins
