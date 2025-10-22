from django.db import models
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from bleach.sanitizer import Cleaner
from bleach.css_sanitizer import CSSSanitizer
from django.contrib.auth.models import Group
from .drive_service import create_associado_folder
from django.apps import apps
from django.db import transaction
from decimal import Decimal
from .utils import format_celular_for_whatsapp
import re
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords

from app_associacao.models import(
    AssociacaoModel,
    ReparticoesModel,
    MunicipiosModel,
    ProfissoesModel,
    CargosModel
)


from core.choices import(
    SEXO_CHOICES,
    ETNIA_CHOICES,
    ESCOLARIDADE_CHOICES,
    ESTADO_CIVIL_CHOICES,
    RECOLHE_INSS_CHOICES,
    SEGURO_DEFESO_CHOICES,
    JA_RECEBEU_DEFESO_ALGUMA_VEZ,
    RELACAO_TRABALHO_CHOICES,
    COMERCIALIZACAO_CHOICES,
    OUTRA_FONTE_RENDA,
    BOLSA_FAMILIA_CHOICES,
    CASA_ONDE_MORA,
    UF_CHOICES,
    EMISSOR_RG_CHOICES,
    STATUS_CHOICES,
    ESPECIES_MARITIMAS,

)

# Create your models here.

class PetrechoPesca(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    
# Create your models here.
class AssociadoModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='associado',
        verbose_name="Usuário Associado"
    )    
    drive_folder_id = models.CharField(max_length=100, blank=True, null=True)
    # Informações Pessoais
    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="CPF"
    )
    senha_gov = models.CharField(
        max_length=128, 
        blank=True, 
        null=True,
        help_text="Senha criptografada para segurança."
    )
    celular = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^\(\d{2}\)\d{5}-\d{4}$',  # Garante que o número seja no formato (XX)XXXXX-XXXX
                'Número inválido. O telefone deve conter 10 ou 11 dígitos, ex: (48)99999-9999.'
            )
        ]
    )   
    celular_correspondencia = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^\(\d{2}\)\d{5}-\d{4}$',  # Garante que o número seja no formato (XX)XXXXX-XXXX
                'Número inválido. O telefone deve conter 10 ou 11 dígitos, ex: (48)99999-9999.'
            )
        ]
    )
    email = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name="E-mail"
    )
    senha_google = models.CharField(
        max_length=128, 
        blank=True, 
        null=True,
        help_text="Senha criptografada para segurança.",
    )
    senha_site = models.CharField(
        max_length=128, 
        blank=True, 
        null=True,
        help_text="Senha criptografada para segurança.",
    )    
    foto = models.ImageField(
        upload_to='fotos_associados/', 
        blank=True, 
        null=True
    )
    apelido = models.CharField(
        max_length=80, 
        blank=True,
        null=True,
        verbose_name="Apelido Carinhoso",
        help_text="Apelido Carinhoso.",
    )     
    sexo_biologico = models.CharField(
        max_length=15, 
        choices=SEXO_CHOICES,
        blank=True,
        default="Não declarado",
        verbose_name="Sexo Biológico"
    )
    etnia = models.CharField(
        max_length=15,
        blank=True,
        choices=ETNIA_CHOICES, 
        default="Não declarado",
        verbose_name="Etnia"
    )
    escolaridade = models.CharField(
        max_length=20,
        blank=True,
        choices=ESCOLARIDADE_CHOICES, 
        default="Não declarado",
        verbose_name="Escolaridade"
    )
    nome_mae = models.CharField(
        max_length=100, 
        verbose_name="Nome da Mãe", 
        blank=True, 
        null=True
    )
    nome_pai = models.CharField(
        max_length=100, 
        verbose_name="Nome do Pai", 
        blank=True, null=True
    )
    estado_civil = models.CharField(
        max_length=50, 
        choices=ESTADO_CIVIL_CHOICES, 
        blank=True, null=True, 
        verbose_name="Estado Civil",
        default="Não declarado"
    )
    profissao = models.ForeignKey(
        ProfissoesModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Profissão"
    )
    recolhe_inss = models.CharField(
        max_length=50, 
        choices=RECOLHE_INSS_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name='Recolhe INSS atualmente?',
        default="Não declarado"
    )
    recebe_seguro = models.CharField(
        max_length=50, 
        choices=SEGURO_DEFESO_CHOICES, 
        blank=True, 
        null=True, 
        default="Não declarado"
    )
    ja_recebeu_defeso_algumavez = models.CharField(
        max_length=50, 
        choices=JA_RECEBEU_DEFESO_ALGUMA_VEZ, 
        blank=True, 
        null=True, 
        verbose_name='Já Recebeu Seguro Defeso Alguma Vez?',
        default="Não declarado"
    )    
    relacao_trabalho = models.CharField(
        choices=RELACAO_TRABALHO_CHOICES,
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Relação de Trabalho",
        default="Não declarado"
    )
    comercializa_produtos = models.CharField(
        choices=COMERCIALIZACAO_CHOICES,
        max_length=250, 
        blank=True, 
        null=True, 
        verbose_name="Comercializa Produtos",
        default="Não declarado"
    )
    outra_fonte_renda = models.CharField(
        choices=OUTRA_FONTE_RENDA,
        max_length=250, 
        blank=True, 
        null=True, 
        verbose_name="Possui outra Fonte de Renda?",
        default="Não declarado"
    )    
    bolsa_familia = models.CharField(
        choices=BOLSA_FAMILIA_CHOICES,
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="Já recebeu Bolsa Família?",
        default="Não declarado"
    )   
    casa_onde_mora = models.CharField(
        choices=CASA_ONDE_MORA,
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="Mora em:",
        default="Não declarado"
    )  
    petrechos_pesca = models.ManyToManyField(
        'PetrechoPesca',
        blank=True,
        verbose_name="Petrechos de Pesca"
    )       
    # Documento RG
    rg_numero = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Número do RG", 
        blank=True, 
        null=True
    )
    rg_orgao = models.CharField(
        max_length=50,
        blank=True,
        choices=EMISSOR_RG_CHOICES,
        default='Não declarado',
        verbose_name="RG-Orgão Emissor"
    )
    rg_data_emissao = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Data Emissão do RG"
    )
    naturalidade = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    data_nascimento = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Data de Nascimento"
    )
    # Documentos/Números Cidadão INSS/NIT/PIS/TITULO
    nit = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        verbose_name="Número do NIT", 
        unique=True
    )
    pis = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        verbose_name="Número do PIS"
    )
    titulo_eleitor = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="Número do Título de Eleitor"
    )
    caepef = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="Número do CAEPEF"
    )
    cei = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="Número do CEI"
    )
   # Documentação Profissional
    rgp = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        verbose_name="Número do RGP", 
        unique=True
    )
    rgp_data_emissao = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Data Emissão do RGP"
    )
    primeiro_registro = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Data Primeiro Registro (RGP)"
    )
    rgp_mpa = models.CharField(
        blank=True, 
        null=True, 
        max_length=12, 
        verbose_name="Mapa do RGP"
    )

    # Documentação de Trabalho
    ctps = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        unique=True,
        verbose_name="Número Carteira Trabalho (CTPS)"
    )
    ctps_serie = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        verbose_name="CTPS - Série"
    )
    ctps_data_emissao = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Data Emissão da CTPS"
    )
    ctps_uf = models.CharField(
        blank=True, 
        null=True, 
        max_length=50, 
        choices=UF_CHOICES, 
        default="Não declarado",
        verbose_name="CTPS UF"
    )
    # Documentação de Hanbilitação
    cnh = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        unique=True, 
        verbose_name="Núm. Registro da CNH"
    )
    cnh_data_emissao = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Data Emissão da CNH"
    )
    cnh_data_validade = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Data Validade da CNH"
    )    
    cnh_uf = models.CharField(
        blank=True, 
        null=True, 
        max_length=50, 
        choices=UF_CHOICES, 
        default="Não declarado",
        verbose_name="CNH UF"
    )
    # Endereço residencial
    logradouro = models.CharField(
        max_length=255, 
        verbose_name="Logradouro", 
        help_text="Ex: Rua, Servidão, Travessa",
        blank=True, 
        null=True
    )
    bairro = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
    )
    numero = models.CharField(
        max_length=10, 
        default="", 
        blank=True, 
        null=True, 
        verbose_name="Número"
    )
    complemento = models.CharField(
        max_length=255, 
        blank=True, 
        null=True
    )
    cep = models.CharField(
        max_length=9,  # Apenas números (sem o hífen)
        validators=[RegexValidator(r'^\d{5}-\d{3}$', 'CEP deve estar no formato 00000-000')],
        default="", 
        blank=True, 
        null=True,
        verbose_name="CEP"
    )
    municipio = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    uf = models.CharField(
        max_length=50, 
        choices=UF_CHOICES, 
        default="Não declarado", 
        blank=True, null=True, 
        verbose_name="Estado"
    )
    # Vínculo
    associacao = models.ForeignKey(
        AssociacaoModel, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True, 
        related_name='associados_associacao',
        verbose_name="Associação"
    )
    reparticao = models.ForeignKey(
        ReparticoesModel, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True, 
        related_name='reparticoes_associados',
        verbose_name="Repartição"
    )
    municipio_circunscricao = models.ForeignKey(
        MunicipiosModel, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='municipios_associados',
        verbose_name="Município de Circunscrição/Atuação"
    )
    data_filiacao = models.DateField(
        null=True,
        verbose_name="Data da Filiação"
    )
    data_desfiliacao = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Data da Desfiliação"
    )    
    status = models.CharField(
        max_length=40, 
        blank=True, 
        null=True, 
        choices=STATUS_CHOICES,
        verbose_name="Status de atividade",
        default="candidato", 
    )
    # Espécies e Quantidades
    especie1 = models.CharField(
        max_length=50, 
        choices=ESPECIES_MARITIMAS, 
        blank=True, 
        null=True, 
        verbose_name="Espécie 1",
        default="Não declarado"
    )
    quantidade1 = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name="Quantidade 1 (Kg)"
    )
    preco1 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Preço por Kg - Espécie 1 (R$)"
    )    
    especie2 = models.CharField(
        max_length=50, 
        choices=ESPECIES_MARITIMAS, 
        blank=True, 
        null=True, 
        verbose_name="Espécie 2",
        default="Não declarado"
    )
    quantidade2 = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name="Quantidade 2 (Kg)"
    )
    preco2 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Preço por Kg - Espécie 2 (R$)"
    )
    especie3 = models.CharField(
        max_length=50, 
        choices=ESPECIES_MARITIMAS, 
        blank=True, 
        null=True, 
        verbose_name="Espécie 3",
        default="Não declarado"
    )
    quantidade3 = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name="Quantidade 3 (Kg)"
    )
    preco3 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Preço por Kg - Espécie 3 (R$)"
    )
    especie4 = models.CharField(
        max_length=50, choices=ESPECIES_MARITIMAS, 
        blank=True, 
        null=True, verbose_name="Espécie 4",
        default="Não declarado"
    )
    quantidade4 = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name="Quantidade 4 (Kg)"
    )
    preco4 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Preço por Kg - Espécie 4 (R$)"
    )    
    especie5 = models.CharField(
        max_length=50, 
        choices=ESPECIES_MARITIMAS, 
        blank=True, null=True, 
        verbose_name="Espécie 5",
        default="Não declarado"
    )
    quantidade5 = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name="Quantidade 5 (Kg)"
    )
    preco5 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Preço por Kg - Espécie 5 (R$)"
    )    
    data_atualizacao = models.DateField(
        auto_now=True
    )
    # Anotações
    content = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Anotações"
    )
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Criação da pasta no Drive, se necessário
        creating = not self.pk
        if creating and not self.drive_folder_id:
            try:
                # Definindo o nome da pasta
                folder_name = self.user.get_full_name() if self.user else "Novo_Associado"
                parent_folder_id = '15Nby8u0aLy1hcjvfV8Ja6w_nSG0yFQ2w'

                # Criar a pasta no Google Drive
                folder_id = create_associado_folder(folder_name, parent_folder_id)
                if folder_id:
                    # Adicionando o sufixo e atribuindo ao campo
                    self.drive_folder_id = f"{folder_id}?lfhs=2"
                    print(f"ID salvo no campo: {self.drive_folder_id}")
                else:
                    print("Erro ao criar a pasta. Nenhum ID foi retornado.")
            except Exception as e:
                print(f"Erro ao criar pasta no Drive: {e}")

        # Salva
        super().save(*args, **kwargs)
        
            
    @property
    def drive_folder_link(self):
        if self.drive_folder_id:
            return f"https://drive.google.com/drive/folders/{self.drive_folder_id}"
        return None
    
    # Método auxiliar para o celular limpo
    def get_celular_clean(self):
        return self.celular.replace('-', '').replace(' ', '') if self.celular else ''
    
    def __str__(self):
        return f"Associado {self.user} (filiado em {self.data_filiacao})"    