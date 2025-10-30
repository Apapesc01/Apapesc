# Despesa de uma Associação
# app_despesas/model
from django.db import models
from django.utils.timezone import now
from app_associacao.models import AssociacaoModel
from django.contrib.auth.models import User 
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings


from core.choices import(
    TIPO_DESPESA_CHOICES,

)


class DespesaAssociacaoModel(models.Model):
    associacao = models.ForeignKey(
        'app_associacao.AssociacaoModel',
        on_delete=models.CASCADE,
        related_name='despesas',
        verbose_name="Associação"
    )
    reparticao = models.ForeignKey(
        'app_associacao.ReparticoesModel',
        on_delete=models.SET_NULL,
        related_name='despesas',
        verbose_name="Repartição",
        blank=True,
        null=True
    )

    tipo_despesa = models.CharField(
        max_length=150,
        blank=True,
        choices=TIPO_DESPESA_CHOICES, 
        default="Outros",
        verbose_name="Tipo de Despesa"
    )    
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor da Despesa")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    numero_nota_fiscal = models.CharField(max_length=150, blank=True, null=True, verbose_name="Número da Nota Fiscal")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    data_lancamento = models.DateTimeField(default=now, verbose_name="Data de Lançamento")
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name='Registros',
        verbose_name="Registrado por"
    )
    pago = models.BooleanField(default=False, verbose_name="Despesa Paga")

    comprovante_nota = models.FileField(
        upload_to='comprovantes_despesas/',
        blank=True,
        null=True,
        verbose_name="Comprovante / Nota Fiscal",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        help_text="Upload do comprovante em PDF, JPG ou PNG."
    )
    data_upload_comprovante = models.DateTimeField(null=True, blank=True, verbose_name="Data do Upload do Comprovante")

    class Meta:
        ordering = ['-data_vencimento']
        verbose_name = "Despesa da Associação"
        verbose_name_plural = "Despesas das Associações"

    def __str__(self):
        return f"{self.get_tipo_despesa_display()} - {self.associacao.nome_fantasia} - R$ {self.valor} - Vencimento: {self.data_vencimento} - Pago: {'Sim' if self.pago else 'Não'}"

    def save(self, *args, **kwargs):
        if self.comprovante_nota and not self.data_upload_comprovante:
            self.data_upload_comprovante = now()
        super().save(*args, **kwargs)

    def esta_vencida(self):
        return now().date() > self.data_vencimento


    def status_display(self):
        return "Pago" if self.pago else "Em Aberto"

    @classmethod
    def pagas(cls):
        return cls.objects.filter(pago=True)

    @classmethod
    def em_aberto(cls):
        return cls.objects.filter(pago=False)
