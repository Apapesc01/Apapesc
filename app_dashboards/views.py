from core.views.base_imports import *
from core.views.app_dashboards_imports import *


class SuperDashboardView(View):
    template_name = 'dashboards/dashboard_superuser.html'

    def get(self, request, *args, **kwargs):
        # ANUIDADES
        anuidades = AnuidadeModel.objects.all().order_by('-ano')

        # 1. Quantidade de anos lançados
        qtd_anos_lancados = anuidades.count()

        # 2. Dados por ano
        dados_por_ano = []
        total_anuidades_aplicadas = 0
        total_valor_aplicado = 0

        for anuidade in anuidades:
            qtd_aplicadas = anuidade.anuidades_associados.count()
            valor_total_ano = qtd_aplicadas * anuidade.valor_anuidade

            total_anuidades_aplicadas += qtd_aplicadas
            total_valor_aplicado += valor_total_ano

            dados_por_ano.append({
                'ano': anuidade.ano,
                'qtd_aplicadas': qtd_aplicadas,
                'valor_total_ano': valor_total_ano,
                'valor_unitario': anuidade.valor_anuidade,
            })
        # ARRECADAÇÃO REAL (soma dos pagamentos)
        from app_anuidades.models import Pagamento, DescontoAnuidade
        total_arrecadado = Pagamento.objects.aggregate(
            total=Sum('valor')
        )['total'] or Decimal('0.00')            
        # VALOR EM ABERTO
        valor_anuidades_aberto = total_valor_aplicado - total_arrecadado
        
        # ASSOCIADOS
        associados = AssociadoModel.objects.all()
        total_cadastrados = associados.count()
        associados_ativos = associados.filter(status='associado_lista_ativo').count()
        associados_aposentados = associados.filter(status='associado_lista_aposentado').count()
        total_pagantes = associados_ativos + associados_aposentados

        # 3. TOTAL ARRECADADO
        from app_anuidades.models import Pagamento, DescontoAnuidade, AnuidadeAssociado
        total_arrecadado = Pagamento.objects.aggregate(total=Sum('valor'))['total'] or 0

        # 4. TOTAL DE DESCONTOS
        total_descontos_concedidos = DescontoAnuidade.objects.aggregate(total=Sum('valor_desconto'))['total'] or 0

        # 5. TOTAL DE ANUIDADES PAGAS (cada associado que pagou uma anuidade conta uma)
        total_anuidades_pagas = AnuidadeAssociado.objects.filter(pago=True).count()
        # 6. TOTAL DE ANUIDADES NÃO PAGAS
        total_anuidades_nao_pagas = AnuidadeAssociado.objects.filter(pago=False).count()

        context = {
            # Anuidades
            'qtd_anos_lancados': qtd_anos_lancados,
            'dados_por_ano': dados_por_ano,
            'total_anuidades_aplicadas': total_anuidades_aplicadas,
            'total_valor_aplicado': total_valor_aplicado,
            'valor_anuidades_aberto': valor_anuidades_aberto,

            # Associados
            'total_cadastrados': total_cadastrados,
            'associados_ativos': associados_ativos,
            'associados_aposentados': associados_aposentados,
            'total_pagantes': total_pagantes,

            # Novos dados financeiros
            'total_arrecadado': total_arrecadado,
            'total_descontos_concedidos': total_descontos_concedidos,
            'total_anuidades_pagas': total_anuidades_pagas,
            'total_anuidades_nao_pagas': total_anuidades_nao_pagas,
        }
        return render(request, self.template_name, context)