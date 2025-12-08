from core.views.base_imports import *
from core.views.app_graficos_imports import *

class GraficosSuperView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'graficos/graficos_superuser.html'
    login_url = '/accounts/login/'
    group_required = [
        'Superuser',
    ]        
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            messages.error(request, "Você não tem permissão para criar uma associação.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        context = {}  # você pode passar dados aqui
        return render(request, self.template_name, context)

class DefesoChartsData(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        # ==============================================================
        # 1) IDENTIFICAR O ÚLTIMO ANO DE CONCESSÃO
        # ==============================================================

        ultimo_ano = (
            SeguroDefesoBeneficioModel.objects
            .order_by('-ano_concessao')
            .values_list('ano_concessao', flat=True)
            .first()
        )

        from datetime import date
        if not ultimo_ano:
            ultimo_ano = date.today().year


        # ==============================================================
        # 2) FILTRAR BASE POR ÚLTIMO ANO
        # ==============================================================

        beneficios_filtrados = SeguroDefesoBeneficioModel.objects.filter(
            ano_concessao=ultimo_ano
        )

        controles_filtrados = ControleBeneficioModel.objects.filter(
            beneficio__ano_concessao=ultimo_ano
        )


        # ==============================================================
        # ----- 1. Benefícios por Espécie -----
        beneficios_especie = (
            beneficios_filtrados
            .values("especie_alvo__nome_popular")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
        especies = [b["especie_alvo__nome_popular"] for b in beneficios_especie]
        especies_totais = [b["total"] for b in beneficios_especie]


        # ----- 2. Benefícios por Estado -----
        beneficios_estado = (
            beneficios_filtrados
            .values("estado")
            .annotate(total=Count("id"))
            .order_by("estado")
        )
        estados = [b["estado"] for b in beneficios_estado]
        estados_totais = [b["total"] for b in beneficios_estado]


        # ----- 3. Benefícios por Ano -----
        beneficios_ano = (
            beneficios_filtrados
            .values("ano_concessao")
            .annotate(total=Count("id"))
            .order_by("ano_concessao")
        )
        anos = [b["ano_concessao"] for b in beneficios_ano]
        anos_totais = [b["total"] for b in beneficios_ano]


        # ==============================================================
        # 4) STATUS DO BENEFÍCIO
        # ==============================================================

        dados_status_beneficio = []
        for key, label in STATUS_BENEFICIO_CHOICES:
            count = controles_filtrados.filter(status_pedido=key).count()
            dados_status_beneficio.append({"label": label, "value": count})


        # ==============================================================
        # 5) CONCEDIDOS x NEGADOS
        # ==============================================================

        concedidos = controles_filtrados.filter(status_pedido="CONCEDIDO").count()
        negados = controles_filtrados.filter(status_pedido="NEGADO").count()

        dados_concedido_negado = {
            "labels": ["Concedidos", "Negados"],
            "values": [concedidos, negados],
        }


        # ==============================================================
        # 6) STATUS DE PROCESSAMENTO
        # ==============================================================

        dados_status_processamento = {
            "Usuário Processando": 0,
            "Processada": 0,
            "Aguardando Processamento": 0,
        }

        for item in controles_filtrados:
            status = item.status_processamento
            dados_status_processamento[status] += 1

        dados_status_processamento = [
            {"label": key, "value": value}
            for key, value in dados_status_processamento.items()
        ]


        # ==============================================================
        # 7) ENTRADA POR MÊS (DAR_ENTRADA)
        # ==============================================================

        entrada_choices_map = dict(DAR_ENTRADA_DEFESO_CHOICES)

        dados_entrada_mes = []
        for key, label in entrada_choices_map.items():
            count = controles_filtrados.filter(dar_entrada=key).count()
            dados_entrada_mes.append({"label": label, "value": count})


        # ==============================================================
        # RETORNO FINAL JSON
        # ==============================================================

        return JsonResponse({
            "ultimo_ano": ultimo_ano,
            "especies": especies,
            "especies_totais": especies_totais,
            "estados": estados,
            "estados_totais": estados_totais,
            "anos": anos,
            "anos_totais": anos_totais,
            "dados_status_beneficio": dados_status_beneficio,
            "dados_concedido_negado": dados_concedido_negado,
            "dados_status_processamento": dados_status_processamento,
            "dados_entrada_mes": dados_entrada_mes,
        })
