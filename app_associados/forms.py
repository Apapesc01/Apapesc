from django import forms
from django.contrib.auth.models import Group
from app_accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.dateformat import DateFormat
from django.forms import DateInput

from core.choices import STATUS_CHOICES

from core.validators import (
    validate_and_format_cpf,
    validate_and_format_celular,
    validate_and_format_cep,
    validate_and_format_cnpj,
)
from .models import (
    AssociadoModel,
)
from app_associacao.models import (
    AssociacaoModel,
    ReparticoesModel,
    MunicipiosModel
)

class AssociadoForm(forms.ModelForm):
    class Meta:
        model = AssociadoModel
        fields = 'user', 'associacao', 'reparticao', 'municipio_circunscricao', 'celular', 'celular_correspondencia', 'email', 'cpf', 'senha_gov', 'data_filiacao', 'content'
        widgets = {
            'data_filiacao': forms.DateInput(attrs={'type': 'date'}),            
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),            
            'data_desfiliacao': forms.DateInput(attrs={'type': 'date'}),
            'municipio_circunscricao': forms.Select(),
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 50, 'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'id': 'id_celular'}),
            'celular_correspondencia': forms.TextInput(attrs={'id': 'id_celular_correspondencia'}),
        }

    def __init__(self, *args, **kwargs):
        user_initial = kwargs.pop('user_initial', None)
        super().__init__(*args, **kwargs)

        # Campos de data
        if self.instance and self.instance.pk:
            if self.instance.data_filiacao:
                self.fields['data_filiacao'].widget.attrs['value'] = self.instance.data_filiacao.strftime('%Y-%m-%d')
            if self.instance.data_nascimento:
                self.fields['data_nascimento'].widget.attrs['value'] = self.instance.data_nascimento.strftime('%Y-%m-%d')
            if self.instance.data_desfiliacao:
                self.fields['data_desfiliacao'].widget.attrs['value'] = self.instance.data_desfiliacao.strftime('%Y-%m-%d')

        # IDs para JS
        self.fields['associacao'].widget.attrs.update({'id': 'id_associacao'})
        self.fields['reparticao'].widget.attrs.update({'id': 'id_reparticao'})
        self.fields['municipio_circunscricao'].widget.attrs.update({'id': 'id_municipio_circunscricao'})

        # Filtro de Repartições com base na associação (caso exista)
        if self.instance and self.instance.associacao:
            self.fields['reparticao'].queryset = ReparticoesModel.objects.filter(associacao=self.instance.associacao)

        # Só popula se for um POST OU se for edição com repartição salva
        if self.data.get('reparticao'):
            try:
                reparticao_id = int(self.data.get('reparticao'))
                reparticao = ReparticoesModel.objects.get(pk=reparticao_id)
                self.fields['municipio_circunscricao'].queryset = reparticao.municipios_circunscricao.all()
            except (ValueError, ReparticoesModel.DoesNotExist):
                self.fields['municipio_circunscricao'].queryset = MunicipiosModel.objects.none()

        elif self.instance.pk and self.instance.reparticao:
            self.fields['municipio_circunscricao'].queryset = self.instance.reparticao.municipios_circunscricao.all()

        else:
            self.fields['municipio_circunscricao'].queryset = MunicipiosModel.objects.none()

        # User inicial
        if user_initial:
            self.fields['user'].initial = user_initial
            self.fields['user'].disabled = True
            
   
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        data_desfiliacao = cleaned_data.get("data_desfiliacao")

        if status == 'desassociado' and not data_desfiliacao:
            raise forms.ValidationError("Por favor, preencha a data de desfiliação.")
        elif status == 'associado':
            cleaned_data['data_desfiliacao'] = None  # limpa

        return cleaned_data
    
    def clean_cpf(self):
        return validate_and_format_cpf(self.cleaned_data['cpf'])
    
    def clean_celular(self):
        celular = self.cleaned_data.get('celular', '')
        return validate_and_format_celular(celular)

    def clean_celular_correspondencia(self):
        celular_correspondencia = self.cleaned_data.get('celular_correspondencia', '')
        return validate_and_format_celular(celular_correspondencia) 

    def clean_cep(self):
        cep = self.cleaned_data.get('cep', '')
        return validate_and_format_cep(cep)


class EditAssociadoForm(forms.ModelForm):
    class Meta:
        model = AssociadoModel
        fields = '__all__'
        widgets = {
            'data_filiacao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_nascimento': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'rg_data_emissao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),            
            'data_desfiliacao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'cnh_data_emissao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'cnh_data_validade': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'ctps_data_emissao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'primeiro_registro': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'rgp_data_emissao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'cnh_data_emissao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'cnh_data_emissao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'municipio_circunscricao': forms.Select(),
            'petrechos_pesca': forms.CheckboxSelectMultiple,
            'celular': forms.TextInput(attrs={'id': 'id_celular'}),
            'celular_correspondencia': forms.TextInput(attrs={'id': 'id_celular_correspondencia'}),            
        }

    def __init__(self, *args, **kwargs):
        user_initial = kwargs.pop('user_initial', None)
        super().__init__(*args, **kwargs)
        
        # Evitar autofill do navegador nos campos dos pais
        if 'nome_mae' in self.fields:
            self.fields['nome_mae'].widget.attrs.update({
                'autocomplete': 'section-parent additional-name',
                'autocapitalize': 'words',
                'inputmode': 'text',
            })
        if 'nome_pai' in self.fields:
            self.fields['nome_pai'].widget.attrs.update({
                'autocomplete': 'section-parent additional-name',
                'autocapitalize': 'words',
                'inputmode': 'text',
            })

        # Dar tokens corretos ao bloco de endereço (ajuda o navegador a não confundir)
        for campo in ['logradouro', 'numero', 'bairro', 'cep', 'municipio_circunscricao']:
            if campo in self.fields:
                token = {
                    'logradouro': 'address-line1',
                    'numero': 'address-line2',
                    'bairro': 'address-level4',
                    'cep': 'postal-code',
                    'municipio_circunscricao': 'address-level2',  # cidade
                }.get(campo, 'off')
                self.fields[campo].widget.attrs.update({
                    'autocomplete': f'section-endereco {token}',
                })        
        
        # Drive
        self.fields['drive_folder_id'].widget.attrs['readonly'] = True

        # IDs para JS
        self.fields['associacao'].widget.attrs.update({'id': 'id_associacao'})
        self.fields['reparticao'].widget.attrs.update({'id': 'id_reparticao'})
        self.fields['municipio_circunscricao'].widget.attrs.update({'id': 'id_municipio_circunscricao'})


        # 🧠 ATUALIZAÇÕES CONDICIONAIS (para editar e POST)
        associacao = None
        reparticao = None

        # 📥 Dados do POST têm prioridade
        if self.data.get('associacao'):
            try:
                associacao = AssociacaoModel.objects.get(pk=self.data.get('associacao'))
            except (ValueError, AssociacaoModel.DoesNotExist):
                pass
        elif self.instance and self.instance.associacao:
            associacao = self.instance.associacao

        if associacao:
            self.fields['reparticao'].queryset = ReparticoesModel.objects.filter(associacao=associacao)
        else:
            self.fields['reparticao'].queryset = ReparticoesModel.objects.none()

        if self.data.get('reparticao'):
            try:
                reparticao = ReparticoesModel.objects.get(pk=self.data.get('reparticao'))
            except (ValueError, ReparticoesModel.DoesNotExist):
                pass
        elif self.instance and self.instance.reparticao:
            reparticao = self.instance.reparticao

        if reparticao:
            self.fields['municipio_circunscricao'].queryset = reparticao.municipios_circunscricao.all()
        else:
            self.fields['municipio_circunscricao'].queryset = MunicipiosModel.objects.none()

        # 🧾 Preenche o usuário (somente para display)
        if user_initial:
            self.fields['user'].initial = user_initial
            self.fields['user'].disabled = True
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        data_desfiliacao = cleaned_data.get("data_desfiliacao")

        if status == 'desassociado' and not data_desfiliacao:
            raise forms.ValidationError("Por favor, preencha a data de desfiliação.")
        elif status == 'associado':
            cleaned_data['data_desfiliacao'] = None  # limpa

        return cleaned_data
    
    def clean_cpf(self):
        return validate_and_format_cpf(self.cleaned_data['cpf'])
    
    def clean_celular(self):
        celular = self.cleaned_data.get('celular', '')
        return validate_and_format_celular(celular)
   
    def clean_celular_correspondencia(self):
        celular_correspondencia = self.cleaned_data.get('celular_correspondencia', '')
        return validate_and_format_celular(celular_correspondencia) 
        
    def clean_cep(self):
        cep = self.cleaned_data.get('cep', '')
        return validate_and_format_cep(cep)    
    
    
    
# Buscas
class AssociadoSearchForm(forms.Form):
    nome = forms.CharField(
        label='Nome',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Digite o nome'})
    )
    associacao = forms.ModelChoiceField(
        label='Associação',
        queryset=AssociacaoModel.objects.all(),
        required=False,
        empty_label='Todas'
    )
    reparticao = forms.ModelChoiceField(
        label='Repartição',
        queryset=ReparticoesModel.objects.all(),
        required=False,
        empty_label='Todas'
    )
    status = forms.ChoiceField(
        label='Status',
        choices=[('', 'Todos')] + STATUS_CHOICES,
        required=False
    )    