from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from app_associados.models import AssociadoModel
from django.db import transaction
import threading
import time

from core.choices import(
    STATUS_EMISSAO_INSS,
    ACESSO_CHOICES,
    MESES,
    STATUS_PROCESSAMENTO
)

class INSSGuiaDoMes(models.Model):
    associado = models.ForeignKey(
        'app_associados.AssociadoModel',
        on_delete=models.CASCADE,
        related_name='guias_inss'
    )
    ano = models.PositiveIntegerField()
    mes = models.CharField(max_length=2, choices=MESES)
    status_emissao = models.CharField(
        max_length=12, choices=STATUS_EMISSAO_INSS, default='pendente'
    )
    status_acesso = models.CharField(
        max_length=40, choices=ACESSO_CHOICES, default='ok'
    )
    data_emissao = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    processada = models.BooleanField(default=False)
    rodada = models.PositiveIntegerField(null=True, blank=True, default=1)
    em_processamento_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='guias_inss_em_processamento'
    )

    history = HistoricalRecords()

    class Meta:
        unique_together = ('associado', 'ano', 'mes', 'rodada')
        ordering = ['-ano', '-mes', 'associado']

    def __str__(self):
        return f"{self.associado} - {self.get_mes_display()}/{self.ano}"

    @property
    def nome_guia(self):
        return f"guia_mes_{self.get_mes_display().lower()}_{self.ano}"

def criar_guias_inss_do_mes(ano, mes, rodada=1):
    ativos = AssociadoModel.objects.filter(
        status='associado_lista_ativo',
        recolhe_inss='Sim'
    )
    criados = 0
    for associado in ativos:
        guia, created = INSSGuiaDoMes.objects.get_or_create(
            associado=associado,
            ano=ano,
            mes=mes,
            rodada=rodada,
            defaults={'status_emissao': 'pendente'}
        )
        if created:
            criados += 1
    return criados

class ProcessamentoINSSModel(models.Model):
    ano = models.PositiveIntegerField()
    mes = models.CharField(max_length=2, choices=MESES)
    rodada = models.PositiveIntegerField(default=1)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processamentos_inss'
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_PROCESSAMENTO,
        default='usuario_processando'
    )
    iniciado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    concluido_em = models.DateTimeField(null=True, blank=True)
    indice_atual = models.PositiveIntegerField(default=0)
    total_associados = models.PositiveIntegerField(default=0)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('ano', 'mes', 'rodada', 'usuario')
        ordering = ['-iniciado_em']

    def __str__(self):
        return f"Processamento INSS {self.mes}/{self.ano} - {self.usuario} (Rodada {self.rodada})"

def pegar_proxima_guia_para_usuario(ano, mes, rodada, usuario):
    with transaction.atomic():
        # tenta encontrar guia em aberto não processada e não em processamento
        guia = INSSGuiaDoMes.objects.select_for_update(skip_locked=True).filter(
            ano=ano,
            mes=mes,
            rodada=rodada,
            processada=False,
            em_processamento_por__isnull=True
        ).first()
        if guia:
            guia.em_processamento_por = usuario
            guia.save(update_fields=['em_processamento_por'])
            return guia
        # se não há nenhuma, retorna None
        return None

def avancar(self):
    """Avança para o próximo associado."""
    if self.indice_atual < len(self.lista_associados) - 1:
        self.indice_atual += 1
        self.save()
        return True
    return False

def finalizar_processamento_guia(guia, usuario):
    guia.processada = True
    guia.em_processamento_por = None
    guia.save(update_fields=['processada', 'em_processamento_por'])


def checar_e_apagar_processamento(ano, mes, rodada):
    restantes = INSSGuiaDoMes.objects.filter(
        ano=int(ano), mes=str(mes).zfill(2), rodada=int(rodada), processada=False
    ).exists()
    if not restantes:
        def apagar():
            print('### Apagando processamento da rodada:', ano, mes, rodada)
            time.sleep(2)
            deleted, _ = ProcessamentoINSSModel.objects.filter(
                ano=int(ano), mes=str(mes).zfill(2), rodada=int(rodada)
            ).delete()
            print('Processamento apagado? Quantos:', deleted)
            INSSGuiaDoMes.objects.filter(
                ano=int(ano), mes=str(mes).zfill(2), rodada=int(rodada)
            ).update(em_processamento_por=None)
            print('Locks de guias limpos!')
        threading.Thread(target=apagar).start()
        return True
    return False



