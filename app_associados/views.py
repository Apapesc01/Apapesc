# Views App Associados
from core.views.base_imports import *
from core.views.app_associados_imports import *


# CREATES ==================================================================
class AssociadoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = AssociadoModel
    form_class = AssociadoForm
    template_name = 'associados/create_associado.html'
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.GET.get('user_id') or None
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            kwargs['user_initial'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associacao_id = self.request.GET.get('associacao_id')
        user_id = self.request.GET.get('user_id')

        if associacao_id:
            from app_associacao.models import AssociacaoModel
            context['associacao_obj'] = get_object_or_404(AssociacaoModel, pk=associacao_id)

        if user_id:
            context['user_obj'] = get_object_or_404(CustomUser, pk=user_id)

        return context

    def form_valid(self, form):
        # Verifica se o usuário foi passado e associa ao associado
        user_id = self.request.GET.get('user_id')
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            form.instance.user = user  # Associa o usuário ao associado

            # Atualiza o e-mail do usuário, se for diferente
            user_email = form.cleaned_data.get('email')
            if user_email and user.email != user_email:
                user.email = user_email
                user.save()
        else:
            messages.error(self.request, "⚠️ Erro: Nenhum usuário selecionado para associação.")
            return self.form_invalid(form)

        # Salva o associado
        self.object = form.save()

        messages.success(self.request, "✅ Associado salvo com sucesso!")

        # Redireciona baseado no botão clicado
        if "save_and_continue" in self.request.POST:
            return redirect(reverse('app_associados:edit_associado', kwargs={'pk': self.object.pk}))
        elif "save_and_view" in self.request.POST:
            return redirect(reverse('app_associados:edit_associado', kwargs={'pk': self.object.pk}))

        return super().form_valid(form)
    
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar o Associado. Verifique os campos obrigatórios.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('app_associados:edit_associado', kwargs={'pk': self.object.pk})

# -----------------------------------------------------------------------------------------
# SINGLES =================================================================================
class AssociadoSingleView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = AssociadoModel
    template_name = 'associados/single_associado.html'
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
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        associado = self.object  # 👈 MOVA ESTA LINHA PARA CIMA

        # DOCUMENTOS ESSENCIAIS E RELACIONADOS
        tipos_doc_essencial = [
            '001_Autodeclaracao_Pesca',
            '002_Autorizacao_Acesso_GOV',
            '003_Autorizacao_Imagem',
            '004_CAEPF',
            '005_CEI',
            '006_CNH',
            '007_Comprovante_Residencia',
            '008_Comprovante_Seguro_Defeso',
            '009_CPF',
            '010_CTPS',
            '011_Declaracao_Residencia_MAPA',
            '012_Declaracao_Veracidade',
            '013_Ficha_Filiacao',
            '014_Foto_3x4',
            '015_Licenca_Embarcacao',
            '016_NIT_Extrato',
            '017_Procuracao_Judicial',
            '018_Procuracao_Administrativa',
            '019_Protocolo_Entrada_RGP',
            '020_RG_Antigo',
            '021_RG_CIN',
            '022_RGP',
            '023_POP',
            '024_TIE',
            '025_Titulo_Eleitor',
        ]

        content_type = ContentType.objects.get_for_model(AssociadoModel)
        documentos_up = UploadsDocs.objects.filter(
            proprietario_content_type=content_type,
            proprietario_object_id=associado.pk
        )

        status_documentos_up = {}
        for tipo in tipos_doc_essencial:
            tem_documento = documentos_up.filter(tipo__nome__iexact=tipo).exists()
            status_documentos_up[tipo] = tem_documento

        context['status_documentos_up'] = status_documentos_up
        # Documentos relacionados ao associado
        context['documentos_up'] = documentos_up 
        # ANUIDADES
        ultimas_anuidades_qs = AnuidadeAssociado.objects.filter(
            associado=associado
        ).select_related('anuidade').order_by('-anuidade__ano')[:3]

        ultimas_anuidades = []
        for aa in ultimas_anuidades_qs:
            total_pago = aa.pagamentos.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
            total_descontos = aa.descontos.aggregate(total=Sum('valor_desconto'))['total'] or Decimal('0.00')
            valor_anuidade = aa.anuidade.valor_anuidade
            status_anuidade = "Paga" if (total_pago + total_descontos) >= valor_anuidade else "Em aberto"
            ultimas_anuidades.append({
                'ano': aa.anuidade.ano,
                'total_pago': total_pago,
                'total_descontos': total_descontos,
                'valor_anuidade': valor_anuidade,
                'status_pagamento': "Paga" if (total_pago + total_descontos) >= valor_anuidade else "Em aberto",
                'status_anuidade': "Paga" if (total_pago + total_descontos) >= valor_anuidade else "Em aberto",  # opcional
            })

        # Status válido para aplicar anuidades
        status_ok = associado.status in ['associado_lista_ativo', 'associado_lista_aposentado']

        # Pega todos os anos de anuidades já aplicadas a esse associado
        anos_aplicados = set(
            associado.anuidades_associados.values_list('anuidade__ano', flat=True)
        )

        # Anos lançados no sistema
        anos_lancados = list(
            AnuidadeModel.objects.order_by('ano').values_list('ano', flat=True)
        )

        # Descobre os anos que devem ser aplicados (da filiação até o ano atual)
        if associado.data_filiacao:
            ano_filiacao = associado.data_filiacao.year
            ano_atual = timezone.now().year
            anos_aplicaveis = [a for a in anos_lancados if ano_filiacao <= a <= ano_atual]
        else:
            anos_aplicaveis = []
        # Anos faltando aplicar
        anos_faltantes = set(anos_aplicaveis) - anos_aplicados


        content_type = ContentType.objects.get_for_model(AssociadoModel)

        uploads = UploadsDocs.objects.filter(
            proprietario_content_type=content_type,
            proprietario_object_id=associado.pk
        ).order_by('tipo__nome')
        
        # INSS:
        context['guias_inss'] = INSSGuiaDoMes.objects.filter(
            associado=associado
        ).order_by('-ano', '-mes', '-rodada')        

        # INSS já aplicado? (Ou seja: este associado já tem guia para TODOS os meses lançados?)
        meses_anos_rodadas = INSSGuiaDoMes.objects.values_list('ano', 'mes', 'rodada').distinct()
        inss_faltando = 0
        for ano, mes, rodada in meses_anos_rodadas:
            if not INSSGuiaDoMes.objects.filter(associado=associado, ano=ano, mes=mes, rodada=rodada).exists():
                inss_faltando += 1
                break
            
        context['inss_aplicado'] = (inss_faltando == 0)
        # Seguro Defeso aplicado
        # Último benefício para o estado do associado
        uf = associado.municipio_circunscricao.uf
        beneficio_defeso_ultimo = (
            SeguroDefesoBeneficioModel.objects
            .filter(estado=uf)
            .order_by('-ano_concessao', '-data_inicio')
            .first()
        )

        defeso_aplicado = False
        if beneficio_defeso_ultimo:
            defeso_aplicado = ControleBeneficioModel.objects.filter(
                associado=associado,
                beneficio=beneficio_defeso_ultimo
            ).exists()
            
        context['defeso_aplicado'] = defeso_aplicado
        context['beneficio_defeso_ultimo'] = beneficio_defeso_ultimo
        
        
        # --- verificar se pode participar do REAP ---
        status_ok_reap = associado.status in ['associado_lista_ativo', 'associado_lista_aposentado']

        # --- REAP: último ano/rodada ---
        ultimo_ano = REAPdoAno.objects.aggregate(Max('ano'))['ano__max']
        reap_disponivel = bool(ultimo_ano)
        reap_aplicado = False
        reap_rodada = None

        if ultimo_ano:
            reap_rodada = REAPdoAno.objects.filter(ano=ultimo_ano).aggregate(Max('rodada'))['rodada__max'] or 1
            reap_aplicado = REAPdoAno.objects.filter(
                associado=associado,
                ano=ultimo_ano,
                rodada=reap_rodada,
            ).exists()

        context.update({
            'status_ok_reap': status_ok_reap,
            'reap_disponivel': reap_disponivel,
            'reap_aplicado': reap_aplicado,
            'reap_ano': ultimo_ano,
            'reap_rodada': reap_rodada,
        })

        # ==== BLOCO DEFESO ====
        uf = associado.municipio_circunscricao.uf if associado.municipio_circunscricao else None
        beneficio_defeso_ultimo = (
            SeguroDefesoBeneficioModel.objects
            .filter(estado=uf)
            .order_by('-ano_concessao', '-data_inicio')
            .first()
        )
        context['beneficio_defeso_ultimo'] = beneficio_defeso_ultimo

        controle_defeso = None
        defeso_form = None
        if beneficio_defeso_ultimo:
            controle_defeso = ControleBeneficioModel.objects.filter(
                associado=associado,
                beneficio=beneficio_defeso_ultimo
            ).first()

            if controle_defeso:
                defeso_form = ControleBeneficioForm(instance=controle_defeso)
            else:
                # Pré-instancia o form com defaults (sem criar no bd)
                defeso_form = ControleBeneficioForm()

        context['controle_defeso'] = controle_defeso
        context['defeso_form'] = defeso_form
        context['defeso_status_elegivel'] = associado.status in ['associado_lista_ativo', 'associado_lista_aposentado']

    
        context['servicos'] = ServicoModel.objects.filter(associado=self.object)
        context['uploads_docs'] = uploads
        context['ultimas_anuidades'] = ultimas_anuidades
        context['status_ok'] = status_ok
        context['anos_faltantes'] = sorted(list(anos_faltantes))
        context['deve_aplicar_anuidades'] = status_ok and anos_faltantes
        context['msg_anuidades_aplicadas'] = not anos_faltantes        
        context['guias_inss'] = INSSGuiaDoMes.objects.filter(associado=associado).order_by('-ano', '-mes', '-rodada')
        context['STATUS_EMISSAO_INSS'] = STATUS_EMISSAO_INSS
        context['ACESSO_CHOICES'] = ACESSO_CHOICES
        # Adiciona embarcações
        context['embarcacoes'] = EmbarcacoesModel.objects.filter(proprietario=associado)

        alerta_user_id = self.request.session.pop('alerta_refiliado_user_id', None)
        if alerta_user_id:
            user_alerta = CustomUser.objects.filter(id=alerta_user_id).first()
            if user_alerta:
                context['alerta_refiliado_user'] = user_alerta
                
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        associado = self.object
        action = request.POST.get('action')
        
        # Verifica se é AJAX e só salva anotações
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            new_content = request.POST.get('content', '').strip()
            if new_content != self.object.content:
                self.object.content = new_content
                self.object.save(update_fields=['content'])
            return JsonResponse({
                'success': True,
                'message': "Anotações salvas com sucesso.",
                'content': self.object.content
            })

        # 1. Edição manual via formulário tradicional
        new_content = request.POST.get('content', '').strip()
        if new_content != self.object.content:
            self.object.content = new_content
            self.object.save(update_fields=['content'])


        # Busca Guias do Associado
        guia_id = request.POST.get('guia_id')
        if guia_id:
            try:
                guia = INSSGuiaDoMes.objects.get(id=guia_id, associado=associado)
                status_emissao = request.POST.get('status_emissao')
                status_acesso = request.POST.get('status_acesso')
                mudou = False
                if status_emissao and status_emissao != guia.status_emissao:
                    guia.status_emissao = status_emissao
                    mudou = True
                if status_acesso and status_acesso != guia.status_acesso:
                    guia.status_acesso = status_acesso
                    mudou = True
                if mudou:
                    guia.save(update_fields=['status_emissao', 'status_acesso'])
                    messages.success(request, f"Status da guia {guia.get_mes_display()}/{guia.ano} atualizado!")
                else:
                    messages.info(request, "Nada foi alterado.")
            except INSSGuiaDoMes.DoesNotExist:
                messages.error(request, "Guia não encontrada para edição.")

        # Aplica as Guias do INSS ao Associado
        if 'aplicar_inss' in request.POST and associado.recolhe_inss == 'Sim':
            # Pega todos os meses/anos já lançados no sistema e aplica
            meses_anos_rodadas = INSSGuiaDoMes.objects.values_list('ano', 'mes', 'rodada').distinct()
            criados = 0
            for ano, mes, rodada in meses_anos_rodadas:
                guia, created = INSSGuiaDoMes.objects.get_or_create(
                    associado=associado,
                    ano=ano,
                    mes=mes,
                    rodada=rodada,
                    defaults={'status_emissao': 'pendente'}
                )
                if created:
                    criados += 1
            if criados:
                messages.success(request, f'{criados} guias INSS aplicadas ao associado!')
            else:
                messages.info(request, 'Nenhuma nova guia INSS criada: o associado já estava incluído em todas as guias.')
            return redirect('app_associados:single_associado', pk=associado.pk)

        # Aplicar Seguro Defeso
        if 'aplicar_defeso' in request.POST and associado.recebe_seguro == 'Recebe':
            # Pegue o estado do associado (ajuste se o campo não for exatamente esse)
            uf = associado.municipio_circunscricao.uf

            # Encontra o benefício MAIS RECENTE lançado para aquele estado
            ultimo_beneficio = (
                SeguroDefesoBeneficioModel.objects
                .filter(estado=uf)
                .order_by('-ano_concessao', '-data_inicio')
                .first()
            )

            aplicados = 0
            if ultimo_beneficio:
                if not ControleBeneficioModel.objects.filter(associado=associado, beneficio=ultimo_beneficio).exists():
                    ControleBeneficioModel.objects.create(
                        associado=associado,
                        beneficio=ultimo_beneficio,
                        status_pedido='EM_PREPARO'
                    )
                    aplicados = 1

            if aplicados:
                messages.success(request, f"Seguro Defeso {ultimo_beneficio.ano_concessao} aplicado ao associado!")
            else:
                messages.info(request, "Nenhum benefício novo a aplicar para o último ano lançado.")

        # Incluir no REAP atual
        if action == 'aplicar_reap':
            ultimo_ano = REAPdoAno.objects.aggregate(Max('ano'))['ano__max']
            if not ultimo_ano:
                messages.error(request, "Não há REAP disponível para aplicar.")
                return redirect(request.path)

            ultima_rodada = REAPdoAno.objects.filter(ano=ultimo_ano).aggregate(Max('rodada'))['rodada__max'] or 1

            obj, created = REAPdoAno.objects.get_or_create(
                associado=self.object,
                ano=ultimo_ano,
                rodada=ultima_rodada,
                defaults={
                    'status_resposta': 'pendente',
                    'processada': False,
                }
            )
            if created:
                messages.success(request, f"Associado incluído no REAP {ultimo_ano}/{ultima_rodada}.")
            else:
                messages.info(request, f"Este associado já estava no REAP {ultimo_ano}/{ultima_rodada}.")
                    
            return redirect('app_associados:single_associado', pk=associado.pk)

                    
        # Só aplica se status ok e POST para aplicar_anuidades
        status_ok = associado.status in ['associado_lista_ativo', 'associado_lista_aposentado']

        if status_ok and 'aplicar_anuidades' in request.POST:
            anos_atuais = set(
                associado.anuidades_associados.values_list('anuidade__ano', flat=True)
            )
            anos_lancados = list(
                AnuidadeModel.objects.order_by('ano').values_list('ano', flat=True)
            )
            ano_filiacao = associado.data_filiacao.year
            ano_atual = timezone.now().year
            anos_aplicaveis = [a for a in anos_lancados if ano_filiacao <= a <= ano_atual]
            anos_faltantes = set(anos_aplicaveis) - anos_atuais

            for ano in anos_faltantes:
                anuidade = AnuidadeModel.objects.get(ano=ano)
                AnuidadeAssociado.objects.create(
                    anuidade=anuidade,
                    associado=associado,
                    valor_pago=Decimal('0.00'),
                    pago=False
                )
            messages.success(request, f"Anuidades {', '.join(str(a) for a in anos_faltantes)} aplicadas com sucesso!")
        else:
            messages.warning(request, "Status do associado não permite aplicar anuidades.")

        # Só permite se clicar no botão do defeso
        if 'salvar_defeso' in request.POST:
            # Regra: só Ativo ou Aposentado podem editar/aplicar defeso
            status_ok = associado.status in ['associado_lista_ativo', 'associado_lista_aposentado']

            if not status_ok:
                messages.error(request, "Este associado não é elegível para operações de Seguro Defeso (status não permitido).")
                return redirect(self.request.path)

            # Pegamos o último benefício do estado
            uf = associado.municipio_circunscricao.uf if associado.municipio_circunscricao else None
            beneficio_defeso_ultimo = (
                SeguroDefesoBeneficioModel.objects
                .filter(estado=uf)
                .order_by('-ano_concessao', '-data_inicio')
                .first()
            )

            if not beneficio_defeso_ultimo:
                messages.error(request, "Não há benefício de Seguro Defeso lançado para o estado deste associado.")
                return redirect(self.request.path)

            # Obtemos (ou criamos) o controle do defeso para este associado e este benefício
            controle, _ = ControleBeneficioModel.objects.get_or_create(
                associado=associado,
                beneficio=beneficio_defeso_ultimo,
                defaults={'status_pedido': 'EM_PREPARO'}
            )

            form = ControleBeneficioForm(request.POST, request.FILES, instance=controle)
            if form.is_valid():
                # opcional: marca lock de processamento no usuário atual enquanto edita
                controle = form.save(commit=False)
                # Se quiser, pode remover o lock ao salvar:
                # controle.em_processamento_por = None
                controle.save()
                messages.success(request, "Dados do Seguro Defeso salvos com sucesso.")
            else:
                # Para reaproveitar exibição dos erros, jogamos no context via messages (ou deixa que o template leia form.errors)
                messages.error(request, "Corrija os erros no formulário do Seguro Defeso.")
                # Para reexibir com erros, renderize via redirect + mensagens (simples) — já é o que estamos fazendo.


        return redirect('app_associados:single_associado', pk=associado.pk)

# -----------------------------------------------------------------------------------------

# EDITS ================================================================

class AssociadoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = AssociadoModel
    form_class = EditAssociadoForm
    template_name = 'associados/edit_associado.html'
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.GET.get('user_id') or None
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            kwargs['user_initial'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associacao_id = self.request.GET.get('associacao_id')
        reparticao_id = self.request.GET.get('reparticao_id')
        user_id = self.request.GET.get('user_id')
        
        associado = self.get_object()
        user = associado.user 
        
        if associacao_id:
            from app_associacao.models import AssociacaoModel
            context['associacao_obj'] = get_object_or_404(AssociacaoModel, pk=associacao_id)

        if reparticao_id:
            from app_associacao.models import ReparticoesModel
            context['reparticao_obj'] = get_object_or_404(AssociacaoModel, pk=reparticao_id)


        if user_id:
            context['user_obj'] = get_object_or_404(CustomUser, pk=user_id)

        context['user_obj'] = user
                        
        return context
    
    def form_valid(self, form):

        # Captura o status antes da alteração
        associado_antes = self.get_object()
        status_antes = associado_antes.status

        # Salva o formulário (altera status etc.)
        response = super().form_valid(form)

        # Se necessário, reatribui usuário
        user_id = self.request.GET.get('user_id')
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            form.instance.user = user

        # Processa ManyToMany
        petrechos_ids = self.request.POST.getlist('petrechos_pesca')
        if petrechos_ids:
            self.object.petrechos_pesca.set(petrechos_ids)
        else:
            self.object.petrechos_pesca.clear()

        # 👇 Aplicações automáticas
        STATUS_VALIDOS = ['associado_lista_ativo', 'associado_lista_aposentado']
        status_depois = form.instance.status
        associado = form.instance

        # ✅ Só aplica benefícios se o status for elegível
        if status_antes != status_depois and status_depois in STATUS_VALIDOS:
            ano_atual = timezone.now().year
            ano_filiacao = associado.data_filiacao.year if associado.data_filiacao else ano_atual

            # 1️⃣ APLICAR ANUIDADES NÃO APLICADAS (somente a partir da nova refiliação)
            anuidades = AnuidadeModel.objects.filter(ano__gte=ano_filiacao)
            aplicadas = 0
            for anuidade in anuidades:
                if anuidade.ano >= ano_filiacao and not AnuidadeAssociado.objects.filter(anuidade=anuidade, associado=associado).exists():
                    AnuidadeAssociado.objects.create(
                        anuidade=anuidade,
                        associado=associado,
                        valor_pago=Decimal('0.00'),
                        pago=False
                    )
                    aplicadas += 1

            if aplicadas:
                messages.success(self.request, f"{aplicadas} anuidade(s) aplicadas automaticamente a partir de {ano_filiacao}.")

            # 2️⃣ APLICAR REAP (último ano e rodada, se existir)
            ultimo_ano = REAPdoAno.objects.aggregate(Max('ano'))['ano__max']
            if ultimo_ano:
                reap_rodada = REAPdoAno.objects.filter(ano=ultimo_ano).aggregate(Max('rodada'))['rodada__max'] or 1
                reap_existe = REAPdoAno.objects.filter(
                    associado=associado,
                    ano=ultimo_ano,
                    rodada=reap_rodada
                ).exists()
                if not reap_existe:
                    REAPdoAno.objects.create(
                        associado=associado,
                        ano=ultimo_ano,
                        rodada=reap_rodada,
                        status_resposta='pendente'
                    )
                    messages.success(self.request, f"REAP {ultimo_ano}/rodada {reap_rodada} aplicado automaticamente.")

            # 3️⃣ VERIFICAR GUIAS INSS
            guias_inss_existem = INSSGuiaDoMes.objects.filter(associado=associado).exists()
            if not guias_inss_existem:
                messages.warning(self.request, "⚠️ Nenhuma guia INSS foi aplicada ainda. Verifique a necessidade de gerar as guias.")

            # 4️⃣ VERIFICAR E APLICAR BENEFÍCIO DEFESO
            uf = associado.municipio_circunscricao.uf if associado.municipio_circunscricao else None
            beneficio_defeso = SeguroDefesoBeneficioModel.objects.filter(
                estado=uf
            ).order_by('-ano_concessao', '-data_inicio').first()

            if beneficio_defeso:
                controle_existe = ControleBeneficioModel.objects.filter(
                    associado=associado,
                    beneficio=beneficio_defeso
                ).exists()

                if not controle_existe:
                    ControleBeneficioModel.objects.create(
                        associado=associado,
                        beneficio=beneficio_defeso,
                    )
                    messages.success(self.request, f"Benefício Defeso de {beneficio_defeso.ano_concessao} aplicado com sucesso.")

        # ✅ Caso contrário (status não elegível, ex: desassociado), nada é aplicado
        else:
            messages.info(self.request, "Status não elegível para aplicação automática de benefícios.")

        # Mensagem final
        messages.success(self.request, 'Associado atualizado com sucesso!')
        return response
        

    def form_invalid(self, form):
        # Em caso de erro, exibe uma mensagem
        messages.error(self.request, 'Erro ao salvar o Associado. Verifique os campos obrigatórios.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('app_associados:single_associado', kwargs={'pk': self.object.pk})
    
# ---------------------------------------------------------------------------------    

# LISTS ==========================================================================
class AssociadoListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = AssociadoModel
    template_name = 'associados/list_associados.html'
    context_object_name = 'associados'
    ordering = ['user__first_name', 'user__last_name']
    group_required = [
        'Superuser',
        'admin_associacao',
        'auxiliar_associacao'
    ]       
    paginate_by = 25  # Opcional, se quiser paginação

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
        queryset = super().get_queryset()
        form = AssociadoSearchForm(self.request.GET)

        if form.is_valid():
            nome = form.cleaned_data.get('nome')
            associacao = form.cleaned_data.get('associacao')
            reparticao = form.cleaned_data.get('reparticao')
            status = form.cleaned_data.get('status')

            if nome:
                queryset = queryset.filter(
                    Q(user__first_name__icontains=nome) | Q(user__last_name__icontains=nome)
                )
            if associacao:
                queryset = queryset.filter(associacao=associacao)
            if reparticao:
                queryset = queryset.filter(reparticao=reparticao)
            if status:
                queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = AssociadoSearchForm(self.request.GET)
        return context


class AssociadoHistoricoView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = AssociadoModel
    template_name = 'associados/historico_associado.html'
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
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associado = self.get_object()
        historico = list(associado.history.all().order_by('-history_date'))

        diffs = []

        for i in range(len(historico) - 1):
            current = historico[i]
            previous = historico[i + 1]
            delta = current.diff_against(previous)
            diffs.append({
                'entry': current,
                'changes': delta.changes,
            })

        # Add final entry (sem comparação possível)
        if historico:
            diffs.append({
                'entry': historico[-1],
                'changes': [],
            })

        context['diffs'] = diffs
        return context
    

# app_associados
class EnviarParaDriveView(View):
    def post(self, request, pk):
        doc = get_object_or_404(UploadsDocs, pk=pk)

        # Verifica se tem pasta associada
        prop = doc.proprietario_object
        folder_id = getattr(prop, 'drive_folder_id', None)

        if not folder_id:
            messages.error(request, "Este associado não possui pasta no Drive.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            upload_file_to_drive(doc.arquivo.path, os.path.basename(doc.arquivo.name), folder_id)
            messages.success(request, "Arquivo enviado para o Google Drive com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao enviar para o Drive: {e}")

        return redirect(request.META.get('HTTP_REFERER', '/'))    
    


def upload_file_to_drive(filepath, filename, parent_folder_id):
    service = get_drive_service()

    file_metadata = {
        'name': filename,
        'parents': [parent_folder_id]
    }

    media = MediaFileUpload(filepath, resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return uploaded_file.get('id')

@login_required
def refiliar_associado(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if not hasattr(user, 'associado'):
        messages.error(request, "Usuário não possui associado vinculado.")
        return redirect('app_associacao:list_users')

    associado = user.associado

    associado.status = 'associado'
    associado.data_filiacao = timezone.now().date()
    associado.data_desfiliacao = None
    associado.save()

    # ✅ Aplicar automaticamente as anuidades existentes se elegível
    STATUS_VALIDOS = ['associado_lista_ativo', 'associado_lista_aposentado']
    if associado.status in STATUS_VALIDOS:
        ano_filiacao = associado.data_filiacao.year
        ano_atual = timezone.now().year

        anuidades = AnuidadeModel.objects.filter(ano__gte=ano_filiacao)

        aplicadas = 0
        for anuidade in anuidades:
            if not AnuidadeAssociado.objects.filter(anuidade=anuidade, associado=associado).exists():
                AnuidadeAssociado.objects.create(
                    anuidade=anuidade,
                    associado=associado,
                    valor_pago=Decimal('0.00'),
                    pago=False
                )
                aplicadas += 1

        if aplicadas:
            messages.info(request, f"{aplicadas} anuidade(s) aplicadas automaticamente.")

    # ⚠️ Alerta permanente enquanto status for "associado"
    request.session['alerta_refiliado_user_id'] = user.id

    messages.success(request, "Usuário refiliado com sucesso.")
    return redirect('app_associados:single_associado', pk=associado.pk)