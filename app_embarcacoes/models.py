from django.db import models
from django.core.validators import MinValueValidator
from app_associados.models import AssociadoModel
from core.choices import (
    TIPO_EMBARCACAO, PROPULSAO, COMBUSTIVEL_CHOICES,
    ALIENACAO_CHOICES, PORTE_EMBARCACAO, SEGURO_DPEM_CHOICES,NOME_LICENCA_CHOICES, ORGAO_EMISSOR_LICENCA
)

class EmbarcacoesModel(models.Model):
    proprietario = models.ForeignKey(
        AssociadoModel,
        on_delete=models.CASCADE,
        related_name='embarcacoes',
        verbose_name='Proprietário',
    )

    destaque_embarcacao_img = models.ImageField(
        upload_to='embarcacoes/destaques/', blank=True, null=True,
        verbose_name='Imagem em destaque da embarcação',
    )

    nome_embarcacao = models.CharField(max_length=100)
    inscricao_embarcacao = models.CharField(
        max_length=100, unique=True, db_index=True, verbose_name='Inscrição'
    )

    # <-- FIX: CharField com max_length e choices (sem on_delete)
    tipo_embarcacao = models.CharField(
        max_length=50, choices=TIPO_EMBARCACAO, null=True, blank=True,
        verbose_name="Tipo de Embarcação",
    )

    validade_tie = models.DateField(verbose_name='Validade da TIE')

    atividade = models.CharField(max_length=100)
    area_navegacao = models.CharField(max_length=100)

    numero_tripulantes = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    numero_passageiros = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    porte = models.CharField(
        max_length=25, choices=PORTE_EMBARCACAO, null=True, blank=True
    )

    cumprimento = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    # Opcional: trocar para DecimalField
    ab_gt = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True,
        verbose_name='Arqueação Bruta (AB/GT)',
        validators=[MinValueValidator(0)]
    )
    boca = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True,
        validators=[MinValueValidator(0)]
    )

    tipo_propulsao = models.CharField(
        max_length=50, choices=PROPULSAO, null=True, blank=True,
        verbose_name="Tipo de Propulsão",
    )

    combustivel = models.CharField(max_length=15, choices=COMBUSTIVEL_CHOICES)

    # Motores (para MVP; em produção, considere uma tabela Motor)
    motor_1 = models.CharField(max_length=100, blank=True, null=True)
    numero_serie_1 = models.CharField(max_length=100, blank=True, null=True)
    potencia_hp1 = models.CharField(max_length=100, blank=True, null=True)

    motor_2 = models.CharField(max_length=100, blank=True, null=True)
    numero_serie_2 = models.CharField(max_length=100, blank=True, null=True)
    potencia_hp2 = models.CharField(max_length=100, blank=True, null=True)

    motor_3 = models.CharField(max_length=100, blank=True, null=True)
    numero_serie_3 = models.CharField(max_length=100, blank=True, null=True)
    potencia_hp3 = models.CharField(max_length=100, blank=True, null=True)

    motor_4 = models.CharField(max_length=100, blank=True, null=True)
    numero_serie_4 = models.CharField(max_length=100, blank=True, null=True)
    potencia_hp4 = models.CharField(max_length=100, blank=True, null=True)

    ano_construcao = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Ano de Construção"
    )
    construtor_nome = models.CharField(max_length=100, blank=True, null=True)
    material_construcao = models.CharField(max_length=100, blank=True, null=True)

    alienacao = models.CharField(
        max_length=5, choices=ALIENACAO_CHOICES, default='nao'
    )

    co_proprietario_nome = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Co-Proprietário'
    )

    municipio_emissao = models.CharField(max_length=100)
    data_emissao = models.DateField()
    data_atualizacao = models.DateField(auto_now=True)

    traves_img = models.ImageField(
        upload_to='embarcacoes/traves/', blank=True, null=True,
        verbose_name='Imagem da Trave (bordo)'
    )
    popa_img = models.ImageField(
        upload_to='embarcacoes/popa/', blank=True, null=True,
        verbose_name='Imagem da Popa'
    )

    # <-- FIX: padronize DPEM
    seguro_dpem = models.CharField(
        max_length=5, choices=SEGURO_DPEM_CHOICES, default='nao',
        verbose_name='Possui DPEM?'
    )
    seguro_dpem_numero = models.CharField(max_length=100, blank=True, null=True)
    seguro_dpem_data_vencimento = models.DateField(blank=True, null=True)

    # Linceça de Pesca
    licenca_nome = models.CharField(
        max_length=50,
        choices=NOME_LICENCA_CHOICES,
        blank=True,
        null=True,
        verbose_name='Nome da Licença'
    )

    orgao_emissor_nome = models.CharField(
        max_length=50,
        choices=ORGAO_EMISSOR_LICENCA,
        blank=True,
        null=True,
        verbose_name='Órgão Emissor'
    )
    codigo_frota = models.CharField(max_length=50, blank=True, null=True)
    inscricao_aut_naval = models.CharField(max_length=100, blank=True, null=True)
    
    validade_licenca_inicial = models.DateField(
        blank=True,
        null=True,
        verbose_name='Validade Inicial da Licença'
    )

    validade_licenca_final = models.DateField(
        blank=True,
        null=True,
        verbose_name='Validade Final da Licença'
    )
        
    # Documentos
    documento_tie = models.FileField(
        upload_to='embarcacoes/documentos/tie/',
        blank=True,
        null=True,
        verbose_name='Documento da TIE'
    )

    documento_licenca = models.FileField(
        upload_to='embarcacoes/documentos/licenca/',
        blank=True,
        null=True,
        verbose_name='Documento da Licença'
    )
    
    content = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['nome_embarcacao']
        verbose_name = 'Embarcação'
        verbose_name_plural = 'Embarcações'

    def __str__(self):
        return f"{self.nome_embarcacao} ({self.inscricao_embarcacao})"

    # Validações úteis
    def clean(self):
        from django.core.exceptions import ValidationError
        from datetime import date

        # validade TIE no passado pode ser permitido, mas avise se quiser
        if self.validade_tie and self.validade_tie < date(1900,1,1):
            raise ValidationError({'validade_tie': 'Data inválida.'})

        if self.data_emissao and self.validade_tie and self.validade_tie < self.data_emissao:
            raise ValidationError({'validade_tie': 'Validade da TIE não pode ser anterior à data de emissão.'})
