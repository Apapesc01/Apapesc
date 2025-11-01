from core.views.app_inss_imports import *
from core.views.base_imports import *


class LancamentosINSSListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = INSSGuiaDoMes
    template_name = 'inss/lancamentos_inss.html'
    context_object_name = 'guias'
    group_required = [
        'Superuser',
        'admin_associacao',
        'auxiliar_associacao'
    ]        

    def dispatch(self, request, *args, **kwargs):
        if not (
            request.user.is_authenticated and 
            (
                request.user.is_superuser or 
                request.user.user_type == 'admin_associacao' or 
                request.user.user_type == 'auxiliar_associacao'
            )
        ):
            messages.error(self.request, "Você não tem permissão para visualizar um usuário.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        ano = self.request.GET.get('ano') or timezone.now().year
        mes = self.request.GET.get('mes') or timezone.now().strftime('%m')
        return INSSGuiaDoMes.objects.filter(ano=ano, mes=mes)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        ano = self.request.GET.get('ano') or timezone.now().year
        mes = self.request.GET.get('mes') or timezone.now().strftime('%m')
        # Descubra a rodada atual (igual já faz)
        rodada = INSSGuiaDoMes.objects.filter(ano=ano, mes=mes).aggregate(Max('rodada'))['rodada__max'] or 1
        # Verifica se há qualquer guia em processamento
        tem_processamento = INSSGuiaDoMes.objects.filter(
            ano=ano, mes=mes, rodada=rodada, em_processamento_por__isnull=False
        ).exists()
        context['tem_processamento'] = tem_processamento
        context['ano_selecionado'] = ano
        context['mes_selecionado'] = mes        
        
        context['anos'] = range(2023, timezone.now().year + 2)
        context['meses'] = MESES
        context['ano_selecionado'] = int(self.request.GET.get('ano', timezone.now().year))
        context['mes_selecionado'] = self.request.GET.get('mes', timezone.now().strftime('%m'))
        return context

    def post(self, request, *args, **kwargs):
        ano = int(request.POST.get('ano') or timezone.now().year)
        mes = request.POST.get('mes') or timezone.now().strftime('%m')
        if mes not in dict(MESES).keys():
            messages.error(request, "Selecione um mês válido para gerar as guias.")
            return redirect(request.path)

        criados = criar_guias_inss_do_mes(ano, mes)
        if criados:
            messages.success(request, f"{criados} guias do INSS criadas para {mes}/{ano}.")
        else:
            messages.info(request, f"Nenhuma nova guia foi criada para {mes}/{ano} (já existem para todos).")
        # Redireciona para manter GET params
        return redirect(f"{request.path}?ano={ano}&mes={mes}")
    
# LISTA - Listagem de Lançamentos - Delete
class ListagemINSSLancamentosView(LoginRequiredMixin, ListView):
    template_name = 'inss/listagem_inss_lancamentos.html'
    context_object_name = 'lancamentos'

    def get_queryset(self):
        return (
            INSSGuiaDoMes.objects
            .values('ano', 'mes', 'rodada')
            .annotate(total=Count('id'))
            .order_by('-ano', '-mes', 'rodada')
        )
class DeletarLancamentoINSSView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ano = request.POST.get('ano')
        mes = request.POST.get('mes')
        rodada = request.POST.get('rodada')

        if ano and mes and rodada:
            guias = INSSGuiaDoMes.objects.filter(ano=ano, mes=mes, rodada=rodada)
            total = guias.count()
            guias.delete()
            messages.success(request, f"{total} guias do lançamento {mes}/{ano} (rodada {rodada}) foram deletadas.")
        else:
            messages.error(request, "Dados incompletos para exclusão.")

        return redirect('app_inss:listagem_inss_lancamentos')    


class ProcessamentoINSSDoMesView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'inss/processamento_manual_inss.html'
    group_required = [
        'Superuser',
        'admin_associacao',
        'auxiliar_associacao'
    ]        

    def dispatch(self, request, *args, **kwargs):
        if not (
            request.user.is_authenticated and 
            (
                request.user.is_superuser or 
                request.user.user_type == 'admin_associacao' or 
                request.user.user_type == 'auxiliar_associacao'
            )
        ):
            messages.error(self.request, "Você não tem permissão para visualizar um usuário.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        # Força o usuário a escolher ANO/MÊS
        ano = request.GET.get('ano')
        mes = request.GET.get('mes')
        if not ano or not mes:
            messages.error(request, "Selecione ano e mês primeiro.")
            return redirect('app_inss:lancamentos_inss')

        ano = int(ano)
        mes = str(mes)

        # Descobre rodada
        ult_rodada = INSSGuiaDoMes.objects.filter(
            ano=ano, mes=mes
        ).aggregate(Max('rodada'))['rodada__max']

        if ult_rodada is None:
            messages.error(request, "Não há guias no mês atual.")
            messages.warning(request, "Você precisa gerar as guias deste mês antes de processar!")
            return redirect('app_inss:lancamentos_inss')

        # Se tem rodada aberta, usa ela. Senão, só permite nova rodada se todas processadas e há ação explícita
        abertas = INSSGuiaDoMes.objects.filter(
            ano=ano, mes=mes, rodada=ult_rodada, processada=False
        ).exists()
        if abertas:
            rodada = ult_rodada
        else:

            messages.info(request, "Todas as guias já foram processadas. Inicie uma nova rodada se desejar.")
            return redirect('app_inss:lancamentos_inss')


        processamento, _ = ProcessamentoINSSModel.objects.get_or_create(
            ano=ano, mes=mes, rodada=rodada, usuario=request.user,
            defaults={'status': 'usuario_processando'}
        )

        guia = INSSGuiaDoMes.objects.filter(
            ano=ano, mes=mes, rodada=rodada, processada=False, em_processamento_por=request.user
        ).first()
        if not guia:
            guia = pegar_proxima_guia_para_usuario(ano, mes, rodada, request.user)

        if not guia:
            processamento.status = 'Processada'
            processamento.concluido_em = timezone.now()
            processamento.save()
            checar_e_apagar_processamento(ano, mes, rodada)
            return redirect('app_inss:lancamentos_inss')

        # Pegue ano, mes, rodada como já faz
        total_guias = INSSGuiaDoMes.objects.filter(
            ano=ano, mes=mes, rodada=rodada
        ).count()

        # Descobrir o índice da guia atual (1-based!)
        if guia:
            guias_ordenadas = list(INSSGuiaDoMes.objects.filter(
                ano=ano, mes=mes, rodada=rodada
            ).order_by('associado__user', 'id'))  # ajuste ordenação se quiser
            guia_index = guias_ordenadas.index(guia) + 1
        else:
            guia_index = None
    
        usuarios_em_processamento = INSSGuiaDoMes.objects.filter(
            ano=ano, mes=mes, rodada=rodada,
            em_processamento_por__isnull=False
        ).values_list('em_processamento_por__username', flat=True).distinct()

        if guia:
            ano = guia.ano
            mes = int(guia.mes)
            associado = guia.associado

            # Buscar meses anteriores no mesmo ano, ordenando do mais antigo para o mais recente
            guias_anteriores = INSSGuiaDoMes.objects.filter(
                associado=associado,
                ano=ano,
                mes__lt=str(mes).zfill(2),   # Somente meses anteriores
                rodada=rodada
            ).order_by('mes')
        else:
            guias_anteriores = []
            
            
        return render(request, self.template_name, {
            'guia': guia,
            'processamento': processamento,
            'ano': ano,
            'mes': mes,
            'rodada': rodada,
            'STATUS_EMISSAO_INSS': STATUS_EMISSAO_INSS,
            'ACESSO_CHOICES': ACESSO_CHOICES,    
            'total_guias': total_guias,
            'guia_index': guia_index,         
            'usuarios_em_processamento': usuarios_em_processamento,
            'guias_anteriores': guias_anteriores,
        })

    def post(self, request):
        ano = int(request.GET.get('ano'))
        mes = str(request.GET.get('mes')).zfill(2)
        rodada = int(request.GET.get('rodada', 1))
        guia_id = request.POST.get('guia_id')

        guia = INSSGuiaDoMes.objects.get(id=guia_id)
        guia.status_emissao = request.POST.get('status_emissao', guia.status_emissao)
        guia.status_acesso = request.POST.get('status_acesso', guia.status_acesso)
        guia.save()
        
        # Atualiza meses anteriores...
        ano_atual = guia.ano
        mes_atual = int(guia.mes)
        associado = guia.associado

        guias_anteriores = INSSGuiaDoMes.objects.filter(
            associado=associado,
            ano=ano_atual,
            mes__lt=str(mes_atual).zfill(2),
            rodada=rodada
        ).order_by('mes')

        for antiga in guias_anteriores:
            novo_status = request.POST.get(f'status_emissao_{antiga.id}')
            if novo_status and novo_status != antiga.status_emissao:
                antiga.status_emissao = novo_status
                antiga.save(update_fields=['status_emissao'])

        action = request.POST.get('action', 'proximo')

        if action == "voltar":
            # Só salva, não finaliza processamento, permanece na rodada
            messages.success(request, "Alterações salvas! Você pode retomar o processamento depois.")
            return redirect('app_inss:lancamentos_inss')

        # Se for 'proximo' (default), segue fluxo normal:
        finalizar_processamento_guia(guia, request.user)
        proxima_guia = pegar_proxima_guia_para_usuario(ano, mes, rodada, request.user)
        if not proxima_guia:
            checar_e_apagar_processamento(ano, mes, rodada)
            return redirect('app_inss:lancamentos_inss')

        processamento = ProcessamentoINSSModel.objects.get(
            ano=ano, mes=mes, rodada=rodada, usuario=request.user
        )

        total_guias = INSSGuiaDoMes.objects.filter(
            ano=ano, mes=mes, rodada=rodada
        ).count()

        guias_ordenadas = list(INSSGuiaDoMes.objects.filter(
            ano=ano, mes=mes, rodada=rodada
        ).order_by('associado__user', 'id'))
        guia_index = guias_ordenadas.index(proxima_guia) + 1

        usuarios_em_processamento = INSSGuiaDoMes.objects.filter(
            ano=ano, mes=mes, rodada=rodada,
            em_processamento_por__isnull=False
        ).values_list('em_processamento_por__username', flat=True).distinct()

        # Meses anteriores da próxima guia:
        ano_atual_proxima = proxima_guia.ano
        mes_atual_proxima = int(proxima_guia.mes)
        associado_proxima = proxima_guia.associado
        guias_anteriores_proxima = INSSGuiaDoMes.objects.filter(
            associado=associado_proxima,
            ano=ano_atual_proxima,
            mes__lt=str(mes_atual_proxima).zfill(2),
            rodada=rodada
        ).order_by('mes')

        return render(request, self.template_name, {
            'guia': proxima_guia,
            'processamento': processamento,
            'ano': ano,
            'mes': mes,
            'rodada': rodada,
            'STATUS_EMISSAO_INSS': STATUS_EMISSAO_INSS,
            'ACESSO_CHOICES': ACESSO_CHOICES,
            'total_guias': total_guias,
            'guia_index': guia_index,
            'usuarios_em_processamento': usuarios_em_processamento,
            'guias_anteriores': guias_anteriores_proxima,
        })

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        ano = request.GET.get('ano') or str(timezone.now().year)
        mes = request.GET.get('mes') or timezone.now().strftime('%m')

        context['ano_selecionado'] = str(ano)
        context['mes_selecionado'] = str(mes)

        return context
    

@require_POST
@login_required
def resetar_processamento(request):
    ano = int(request.GET.get('ano'))
    mes = str(request.GET.get('mes')).zfill(2)
    rodada = INSSGuiaDoMes.objects.filter(ano=ano, mes=mes).aggregate(Max('rodada'))['rodada__max'] or 1

    qs = INSSGuiaDoMes.objects.filter(ano=ano, mes=mes, rodada=rodada)
    # Aqui reseta só os campos de processamento!
    updated = qs.update(processada=False, em_processamento_por=None)
    messages.success(request, f"{updated} guias resetadas para {mes}/{ano}, rodada {rodada}!")
    return redirect(f"{reverse('app_inss:lancamentos_inss')}?ano={ano}&mes={mes}")