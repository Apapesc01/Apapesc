
# Views - App Anuidades
from core.views.base_imports import *
from core.views.app_anuidades_imports import *


class CreateAnuidadeView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = AnuidadeModel
    form_class = AnuidadeForm
    template_name = 'anuidades/create_anuidade.html'
    success_url = reverse_lazy('app_anuidades:list_anuidades')  # Ajuste para sua URL real
    group_required = [
        'Superuser',
    ]   
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            messages.error(request, "Você não tem permissão para criar uma associação.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)    
    
    def form_valid(self, form):
        # Salva a Anuidade primeiro
        anuidade = form.save(commit=False)
        anuidade.save()
        # Atribui a todos os associados ativos/aposentados, conforme regras
        anuidade.atribuir_anuidades_associados()
        messages.success(self.request, f"Anuidade de {anuidade.ano} criada e atribuída com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao Criar a Anuiade. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)    


class LancamentosAnuiadesListView(LoginRequiredMixin, GroupRequiredMixin, ListView)    :
    model = AnuidadeModel
    template_name = 'anuidades/list_anuidades.html'
    context_object_name = 'anuidades'
    group_required = [
        'Superuser',
    ]   
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            messages.error(request, "Você não tem permissão para criar uma associação.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Total de anuidades
        context['qtd_anuidades'] = AnuidadeModel.objects.count()
        # Soma total dos valores
        context['valor_total_anuidades'] = AnuidadeModel.objects.aggregate(
            total=Sum('valor_anuidade')
        )['total'] or 0
        return context    



class AnuidadeAssociadoSingleView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = AssociadoModel
    template_name = 'anuidades/anuidade_associado.html'
    context_object_name = 'associado'
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
    
    def form_valid(self, form):
        messages.success(self.request, f"pagemento Registrado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro registrar o pagamento. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associado = self.object
        anuidades = AnuidadeAssociado.objects.filter(associado=associado).select_related('anuidade').order_by('-anuidade__ano')

        # TOTAIS GLOBAIS
        total_pago_geral = Decimal('0.00')
        total_descontos_geral = Decimal('0.00')
        saldo_devedor_geral = Decimal('0.00')
        
        anuidade_infos = []
        for aa in anuidades:
            pagamentos = aa.pagamentos.order_by('-data_pagamento')
            descontos = aa.descontos.order_by('-data_concessao')

            total_pago = pagamentos.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
            total_descontos = descontos.aggregate(total=Sum('valor_desconto'))['total'] or Decimal('0.00')
            valor_anuidade = aa.anuidade.valor_anuidade
            saldo_devedor = max(valor_anuidade - total_descontos - total_pago, Decimal('0.00'))
            status = "PAGA" if saldo_devedor <= 0 else "EM ABERTO"

            # Somando nos totais GERAIS
            total_pago_geral += total_pago
            total_descontos_geral += total_descontos
            saldo_devedor_geral += saldo_devedor

            anuidade_infos.append({
                'aa': aa,
                'pagamentos': pagamentos,
                'descontos': descontos,
                'total_pago': total_pago,
                'total_descontos': total_descontos,
                'valor_anuidade': valor_anuidade,
                'saldo_devedor': saldo_devedor,
                'status_anuidade': status,
                'pagamento_form': PagamentoForm(),
                'desconto_form': DescontoAnuidadeForm(),
            })

        context['anuidade_infos'] = anuidade_infos
        context['total_pago_geral'] = total_pago_geral
        context['total_descontos_geral'] = total_descontos_geral
        context['saldo_devedor_geral'] = saldo_devedor_geral
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        associado = self.object
        anuidades = AnuidadeAssociado.objects.filter(associado=associado)
        
        anuidade_id = request.POST.get('anuidade_id')
        aa = anuidades.get(pk=anuidade_id)
        
        if 'pagar' in request.POST:
            form = PagamentoForm(request.POST, request.FILES)
            if form.is_valid():
                pagamento = Pagamento(
                    anuidade_associado=aa,
                    valor=form.cleaned_data['valor'],
                    comprovante_up=form.cleaned_data.get('comprovante_up'),
                    registrado_por=request.user
                )
                try:
                    pagamento.full_clean()
                    pagamento.save()
                    aa.atualizar_status_pagamento()
                    messages.success(request, "Pagamento lançado com sucesso!")

                except ValidationError as e:
                    messages.error(request, "; ".join(e.messages))
                    form.add_error(None, "; ".join(e.messages))
                    context = self.get_context_data()
                    for info in context['anuidade_infos']:
                        if info['aa'].pk == aa.pk:
                            info['pagamento_form'] = form
                    return self.render_to_response(context)                
            else:
                for erro in form.errors.values():
                    messages.error(request, erro)
                return self.get(request, *args, **kwargs)


        if 'descontar' in request.POST:
            form = DescontoAnuidadeForm(request.POST)
            if form.is_valid():
                # BLOQUEIA desconto em anuidade quitada:
                if aa.pago:
                    msg = "Não é permitido lançar desconto em anuidade já quitada!"
                    messages.error(request, msg)
                    form.add_error(None, msg)
                    context = self.get_context_data()
                    for info in context['anuidade_infos']:
                        if info['aa'].pk == aa.pk:
                            info['desconto_form'] = form
                    return self.render_to_response(context)
                
                # Se não está paga, pode lançar desconto normalmente
                desconto = DescontoAnuidade(
                    anuidade_associado=aa,
                    valor_desconto=form.cleaned_data['valor_desconto'],
                    motivo=form.cleaned_data['motivo'],
                    concedido_por=request.user
                )
                try:
                    desconto.full_clean()
                    desconto.save()
                    aa.atualizar_status_pagamento()
                    messages.success(request, "Desconto lançado com sucesso!")
                except ValidationError as e:
                    messages.error(request, "; ".join(e.messages))
                    form.add_error(None, "; ".join(e.messages))
                    context = self.get_context_data()
                    for info in context['anuidade_infos']:
                        if info['aa'].pk == aa.pk:
                            info['desconto_form'] = form
                    return self.render_to_response(context)
            else:
                for erro in form.errors.values():
                    messages.error(request, erro)
                context = self.get_context_data()
                for info in context['anuidade_infos']:
                    if info['aa'].pk == aa.pk:
                        info['desconto_form'] = form
                return self.render_to_response(context)


            
        return redirect(reverse('app_anuidades:anuidade_associado_singular', args=[associado.pk]))



class AnuidadesListaBuscaView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = AnuidadeAssociado
    template_name = 'anuidades/anuidades_list_searchs.html'
    context_object_name = 'resultados'
    group_required = [
        'Superuser',
        'admin_associacao',

    ]    
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and (request.user.is_superuser or request.user.user_type == 'admin_associacao')):
            messages.error(self.request, "Você não tem permissão para visualizar essa Página.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)  
    
    def get_queryset(self):
        ano = self.request.GET.get('ano')
        associacao_id = self.request.GET.get('associacao')
        reparticao_id = self.request.GET.get('reparticao')
        status = self.request.GET.get('status')

        queryset = AnuidadeAssociado.objects.select_related(
            'associado', 'anuidade', 'associado__associacao', 'associado__reparticao'
        )

        # 🔹 FILTRO: ANO (quando não é "Todos")
        if ano and ano != "Todos":
            ano = int(ano)
            queryset = queryset.filter(anuidade__ano=ano)

        # 🔹 FILTRO: ASSOCIAÇÃO
        if associacao_id not in ("", "Todas", None):
            queryset = queryset.filter(associado__associacao_id=int(associacao_id))

        # 🔹 FILTRO: REPARTIÇÃO
        if reparticao_id not in ("", "Todas", None):
            queryset = queryset.filter(associado__reparticao_id=int(reparticao_id))

        ano_atual = timezone.now().year

        # --------------------------
        # 🔹 FILTRO STATUS
        # --------------------------

        if status == "pagos_ano":
            if ano and ano != "Todos":
                queryset = queryset.filter(pago=True)
            else:
                messages.warning(self.request, "Selecione um ano para filtrar pagos do ano.")
                return queryset.none()

        elif status == "abertos_ano":
            if ano and ano != "Todos":
                queryset = queryset.filter(pago=False)
            else:
                messages.warning(self.request, "Selecione um ano para filtrar em aberto do ano.")
                return queryset.none()

        elif status == "em_atraso":
            queryset = queryset.filter(anuidade__ano__lt=ano_atual, pago=False)

        elif status == "em_dia":
            associados_com_debito = AssociadoModel.objects.filter(
                anuidades_associados__anuidade__ano__lte=ano_atual,
                anuidades_associados__pago=False
            ).values_list("id")

            queryset = queryset.exclude(associado_id__in=associados_com_debito)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Para preencher selects/filtros do template:
        context['anos'] = AnuidadeModel.objects.values_list('ano', flat=True).order_by('-ano')
        context['associacoes'] = AssociacaoModel.objects.all()
        context['reparticoes'] = ReparticoesModel.objects.all()
        context['ano_atual'] = timezone.now().year
        # Mantém os filtros selecionados
        context['filtros'] = {
            'ano': self.request.GET.get('ano') or '',
            'associacao': self.request.GET.get('associacao') or '',
            'reparticao': self.request.GET.get('reparticao') or '',
            'status': self.request.GET.get('status') or '',
        }
        return context
