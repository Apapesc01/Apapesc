from django.urls import path
from . import views

app_name = 'app_defeso'

urlpatterns = [
    path('defeso/lancamento/', views.DefesosLancamentoView.as_view(), name='lancamento_defeso'),
    # Creates
    path('create-benfício/', views.SeguroDefesoBeneficioCreateView.as_view(), name='create_beneficio'),
    path('create-decreto/', views.DecretoCreateView.as_view(), name='create_decreto'),
    path('create-periodo/', views.PeriodoCreateView.as_view(), name='create_periodo'),
    path('create-portaria/', views.PortariasCreateView.as_view(), name='create_portaria'),
    path('create-especie/', views.EspecieCreateView.as_view(), name='create_especie'),
    path('create-lei-federal/', views.LeiFederalCreateView.as_view(), name='create_lei_federal'),
    path('create-instrucao-normativa/', views.InstrucoesNormativasCreateView.as_view(), name='create_instrucao_normativa'),
    # Controles e Processamento
    path('controle/<int:pk>/edit/', views.ControleBeneficioEditView.as_view(), name='controle_beneficio_edit'),
    path('processamento/proximo/', views.proximo_controle_para_processar, name='proximo_controle_para_processar'),
    path('processamento/resetar-rodada/', views.resetar_rodada_processamento, name='resetar_rodada_processamento'),
    path('painel-defeso/', views.PainelDefesoStatusView.as_view(), name='painel_status_defeso'),
 
    path('normativos/', views.NormativosDefesoResumoView.as_view(), name='normativos_resumo'),
]
