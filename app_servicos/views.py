from core.views.base_imports import *
from core.views.app_servicos_imports import *


class ServicoCreateView(CreateView):
    model = ServicoModel
    form_class = ServicoForm
    template_name = 'servicos/create_servico.html'
    success_url = reverse_lazy('app_servicos:single_servico')

    def dispatch(self, request, *args, **kwargs):
        self.associado = get_object_or_404(AssociadoModel, pk=kwargs['associado_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['associado'] = self.associado
        initial['associacao'] = self.associado.associacao
        initial['reparticao'] = self.associado.reparticao
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['associado'].queryset = AssociadoModel.objects.filter(pk=self.associado.pk)
        form.fields['associado'].initial = self.associado
        form.fields['associado'].widget.attrs['readonly'] = True
        form.fields['associacao'].widget.attrs['readonly'] = True
        form.fields['reparticao'].widget.attrs['readonly'] = True
        return form

    def form_valid(self, form):
        # Garante vínculo
        form.instance.associado = self.associado
        form.instance.associacao = self.associado.associacao
        form.instance.reparticao = self.associado.reparticao
        form.instance.criado_por = self.request.user

        # ... (seu código)
        if not form.instance.status_servico:
            default_status = {
                "assessoria_administrativa": "agendada",
                "assessoria_processo_paa": "agendada",
                "assessoria_processo_pronaf": "agendada",
                "emissao_tie": "pendente",
                "emissao_rgp": "pendente",
                "emissao_licanca_pesca": "pendente",
                'emissao_pop': "pendente",
                "consultoria_geral": "agendada",
            }
            form.instance.status_servico = default_status.get(form.instance.tipo_servico, '')
            
        response = super().form_valid(form)

        # Se o associado precisar de entrada financeira
        if self.associado.status in STATUS_COBRANCA:
            return redirect(reverse('app_servicos:create_entrada', kwargs={'servico_id': self.object.id}))
        else:
            return redirect(reverse('app_servicos:single_servico', kwargs={'pk': self.object.pk}))

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['associado'] = self.associado
        return context
    
    def get_success_url(self):
        return reverse('app_servicos:single_servico', kwargs={'pk': self.object.pk})
        

class ServicoUpdateView(UpdateView):
    model = ServicoModel
    form_class = ServicoForm
    template_name = 'servicos/edit_servico.html'


    def dispatch(self, request, *args, **kwargs):
        self.servico = get_object_or_404(ServicoModel, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['associado'].queryset = AssociadoModel.objects.filter(pk=self.servico.associado.pk)
        form.fields['associado'].initial = self.servico.associado
        form.fields['associado'].widget.attrs['readonly'] = True
        form.fields['associacao'].widget.attrs['readonly'] = True
        form.fields['reparticao'].widget.attrs['readonly'] = True
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse('app_servicos:single_servico', kwargs={'pk': self.servico.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servico'] = self.servico
        context['associado'] = self.servico.associado 
        context['associacao'] = self.servico.associacao
        context['reparticao'] = self.servico.reparticao
        return context
    
    def get_success_url(self):
        return reverse('app_servicos:single_servico', kwargs={'pk': self.object.pk})




class ServicoSingleView(DetailView):
    model = ServicoModel
    template_name = 'servicos/single_servico.html'
    context_object_name = 'servico'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        content = request.POST.get('content', '').strip()
        msg = ""
        status = 200
        if content != (self.object.content or ''):
            self.object.content = content
            self.object.save(update_fields=['content', 'ultima_alteracao'])
            msg = "Anotações salvas com sucesso!"
            success = True
        else:
            msg = "Nenhuma alteração detectada."
            success = True

        # Se AJAX, retorna JSON:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': success,
                'message': msg,
            }, status=status)

        # Se não for AJAX, segue fluxo tradicional (redirect)
        messages.success(request, msg)
        return redirect(self.request.path)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associado = self.object.associado
        entrada = None
        entrada_form = None
        try:
            entrada = self.object.entrada_servico
            entrada_form = EntradaFinanceiraForm(instance=entrada)
        except EntradaFinanceiraModel.DoesNotExist:
            pass
        
        context['entrada'] = entrada
        context['entrada_form'] = entrada_form
        
        # Corrija aqui:
        if entrada:
            valor_pendente = entrada.valor - (entrada.valor_pagamento or 0)
        else:
            valor_pendente = 0
        context['valor_pendente'] = valor_pendente
        
        tipos_doc_essencial = [
            '001_Auto_Declaração_Pesca', 
            '002_Autorização_ACESSO_GOV_ASS_Associado',  
            '003_Autorização_IMAGEM_ASS_Associado',   
            '004_CAEPF',  
            '005_CEI',  
            '006_CNH_Cart_Motorista',  
            '007_Comp_Resid_LUZ_AGUA_FATURAS',  
            '008_Comp_SEGURO_DEFESO',  
            '009_CPF_Pessoa_Física',  
            '010_CTPS_Cart_Trabalho', 
            '011_Declaração_Residência_MAPA',  
            '012_Ficha_Req_Filiação_ASS_PRESID_JUR', 
            '013_Ficha_Req_Filiação_ASS_Associado',  
            '014_Foto_3x4', 
            '015_Licença_Embarcação',  
            '016_NIT_Extrato',  
            '017_Procuração_AD_JUDICIA',  
            '018_Procuracao_ADMINISTRATIVA',  
            '019_Protocolo_ENTRADA_RGP',  
            '020_RG_Identidade_CIN',
            '021_RGP_Cart_Pescador',
            '021_TIE_Titulo_Embarcação',
            '022_Titulo_Eleitor',
        ]

        documentos_up = UploadsDocs.objects.filter(
            proprietario_object_id=associado.pk,
            proprietario_content_type=ContentType.objects.get_for_model(type(associado)),
            tipo__nome__in=tipos_doc_essencial
        ).select_related('tipo')
        context['documentos_essenciais_up'] = documentos_up        
        context['uploads_docs'] = context['documentos_essenciais_up']  # Se já passou acima!

        context['associado'] = self.object.associado 
        return context
        
class ServicoListView(ListView):
    model = ServicoModel
    template_name = 'servicos/list_servicos.html'
    context_object_name = 'servicos'

    



# ENTRADAS
class EntradaCreateView(CreateView):
    model = EntradaFinanceiraModel
    form_class = EntradaFinanceiraForm
    template_name = 'servicos/create_entrada.html'

    def dispatch(self, request, *args, **kwargs):
        self.servico = get_object_or_404(ServicoModel, pk=kwargs['servico_id'])
        # Bloqueia caso serviço não seja de status que precisa de entrada
        if not self.servico.precisa_entrada_financeira():
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Não é permitido criar entrada financeira para esse serviço.")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['servico'] = self.servico
        initial['valor'] = self.servico.valor
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['servico'].queryset = ServicoModel.objects.filter(pk=self.servico.pk)
        form.fields['servico'].initial = self.servico

        return form

    def form_valid(self, form):
        form.instance.servico = self.servico
        response = super().form_valid(form)
        # Só depois do save!
        self.object.calcular_pagamento()
        return redirect(reverse('app_servicos:single_servico', kwargs={'pk': self.servico.pk}))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['entrada'] = self.servico  # Para mostrar no template
        context['servico'] = self.servico  # Se quiser usar também
        return context

    def get_success_url(self):
        return reverse('app_servicos:single_servico', kwargs={'pk': self.servico.pk})


class EditarEntradaView(UpdateView):
    model = EntradaFinanceiraModel
    form_class = EntradaFinanceiraForm
    template_name = 'servicos/edit_entrada.html'

    def dispatch(self, request, *args, **kwargs):
        self.entrada = get_object_or_404(EntradaFinanceiraModel, pk=kwargs['pk'])
        self.servico = self.entrada.servico
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['servico'].queryset = ServicoModel.objects.filter(pk=self.servico.pk)
        form.fields['servico'].initial = self.servico
        return form

    def form_valid(self, form):
        form.instance.servico = self.servico
        response = super().form_valid(form)
        # Só depois do save!
        self.object.calcular_pagamento()
        return redirect(reverse('app_servicos:single_servico', kwargs={'pk': self.servico.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entrada'] = self.entrada  # Para mostrar no template
        context['servico'] = self.servico  # Se quiser usar também
        return context

    def get_success_url(self):
        return reverse('app_servicos:single_servico', kwargs={'pk': self.servico.pk})
    

class RegistrarPagamentoEntradaView(CreateView):
    model = PagamentoEntrada
    form_class = PagamentoEntradaForm
    template_name = 'servicos/registrar_pagamento_entrada.html'

    def dispatch(self, request, *args, **kwargs):
        self.servico = get_object_or_404(ServicoModel, pk=kwargs['servico_id'])
        self.entrada = getattr(self.servico, 'entrada_servico', None)
        if not self.entrada:
            from django.http import Http404
            raise Http404("Entrada financeira não encontrada para este serviço.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        # Assim o form sabe qual serviço está validando
        return {'servico': self.servico}
    
    def form_valid(self, form):
        form.instance.servico = self.servico
        form.instance.registrado_por = self.request.user
        response = super().form_valid(form)
        # Recalcula o status da entrada
        self.entrada.calcular_pagamento()
        return redirect(reverse('app_servicos:single_servico', kwargs={'pk': self.servico.pk}))
    
    def get_success_url(self):
            return reverse('app_servicos:single_servico', kwargs={'pk': self.servico.pk})    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servico'] = self.servico
        context['entrada'] = self.entrada
        context['pagamentos'] = self.servico.pagamentos.all()
        return context
