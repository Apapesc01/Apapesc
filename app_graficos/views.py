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

        # ----- 1. Benefícios por Espécie -----
        beneficios_especie = (
            SeguroDefesoBeneficioModel.objects
            .values("especie_alvo__nome_popular")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
        especies = [b["especie_alvo__nome_popular"] for b in beneficios_especie]
        especies_totais = [b["total"] for b in beneficios_especie]

        # ----- 2. Benefícios por Estado -----
        beneficios_estado = (
            SeguroDefesoBeneficioModel.objects
            .values("estado")
            .annotate(total=Count("id"))
            .order_by("estado")
        )
        estados = [b["estado"] for b in beneficios_estado]
        estados_totais = [b["total"] for b in beneficios_estado]

        # ----- 3. Benefícios por Ano -----
        beneficios_ano = (
            SeguroDefesoBeneficioModel.objects
            .values("ano_concessao")
            .annotate(total=Count("id"))
            .order_by("ano_concessao")
        )
        anos = [b["ano_concessao"] for b in beneficios_ano]
        anos_totais = [b["total"] for b in beneficios_ano]

        # 1️⃣ Status do Benefício
        dados_status_beneficio = []
        for key, label in STATUS_BENEFICIO_CHOICES:
            count = ControleBeneficioModel.objects.filter(status_pedido=key).count()
            dados_status_beneficio.append({"label": label, "value": count})

        # 2️⃣ Concedidos x Negados
        concedidos = ControleBeneficioModel.objects.filter(status_pedido="CONCEDIDO").count()
        negados = ControleBeneficioModel.objects.filter(status_pedido="NEGADO").count()
        dados_concedido_negado = {
            "labels": ["Concedidos", "Negados"],
            "values": [concedidos, negados],
        }

        # 3️⃣ Status de Processamento — corrigido
        controle = ControleBeneficioModel.objects.all()

        dados_status_processamento = {
            "Usuário Processando": 0,
            "Processada": 0,
            "Aguardando Processamento": 0,
        }

        for item in controle:
            status = item.status_processamento  # usa a property
            dados_status_processamento[status] += 1

        # transformar para o formato usado no JS
        dados_status_processamento = [
            {"label": key, "value": value}
            for key, value in dados_status_processamento.items()
        ]

        return JsonResponse({
            "especies": especies,
            "especies_totais": especies_totais,
            "estados": estados,
            "estados_totais": estados_totais,
            "anos": anos,
            "anos_totais": anos_totais,
            "dados_status_beneficio": dados_status_beneficio,
            "dados_concedido_negado": dados_concedido_negado,
            "dados_status_processamento": dados_status_processamento,
        })

