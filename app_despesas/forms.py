from django import forms
from .models import DespesaAssociacaoModel
from django.forms import DateInput
from app_associacao.models import ReparticoesModel, AssociacaoModel

class DespesaAssociacaoForm(forms.ModelForm):
    class Meta:
        model = DespesaAssociacaoModel
        fields = [
            'associacao',
            'reparticao',
            'tipo_despesa',
            'valor',
            'descricao',
            'numero_nota_fiscal',
            'data_vencimento',
            'data_lancamento',
            'pago',
            'comprovante_nota'
        ]
        widgets = {
            'data_vencimento': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_lancamento': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'valor': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se necessário, você pode filtrar associações e repartições aqui
        self.fields['associacao'].widget.attrs.update({'id': 'id_associacao'})
        self.fields['reparticao'].widget.attrs.update({'id': 'id_reparticao'})
        # Filtro de Repartições com base na associação (caso exista)
        if self.instance and hasattr(self.instance, 'associacao') and self.instance.associacao:
            self.fields['reparticao'].queryset = ReparticoesModel.objects.filter(associacao=self.instance.associacao)
        else:
            self.fields['reparticao'].queryset = ReparticoesModel.objects.none()


        self.fields['tipo_despesa'].widget.attrs.update({'class': 'form-control'})
        self.fields['valor'].widget.attrs.update({'class': 'form-control'})
        self.fields['numero_nota_fiscal'].widget.attrs.update({'class': 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})
        self.fields['data_vencimento'].widget.attrs.update({'class': 'form-control'})
        self.fields['data_lancamento'].widget.attrs.update({'class': 'form-control'})
        self.fields['pago'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['comprovante_nota'].widget.attrs.update({'class': 'form-control-file'})



class FiltroDespesasForm(forms.Form):
    associacao = forms.ModelChoiceField(
        queryset=AssociacaoModel.objects.all(),
        required=False,
        label="Associação",
        widget=forms.Select(attrs={'id': 'id_associacao', 'class': 'form-control'})
    )

    reparticao = forms.ModelChoiceField(
        queryset=ReparticoesModel.objects.none(),  # será preenchido via JS
        required=False,
        label="Repartição",
        widget=forms.Select(attrs={'id': 'id_reparticao', 'class': 'form-control'})
    )

    pago = forms.ChoiceField(
        choices=(
            ('', 'Todos'),
            ('true', 'Pagos'),
            ('false', 'Em aberto'),
        ),
        required=False,
        label="Status do Pagamento",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        associacao_id = self.data.get('associacao') or self.initial.get('associacao')
        if associacao_id:
            self.fields['reparticao'].queryset = ReparticoesModel.objects.filter(associacao_id=associacao_id)