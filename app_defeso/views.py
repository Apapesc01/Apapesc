from core.views.base_imports import *
from core.views.app_defeso_imports import *


class DefesosLancamentoView(View):
    template_name = 'defeso/defesos.html'

    def get(self, request):
        beneficio_id = request.GET.get('beneficio')
        beneficios = SeguroDefesoBeneficioModel.objects.all().order_by('-ano_concessao', '-data_inicio')
        associados_beneficiados = []
        beneficio = None
        mostrar_reset = False
        mostrar_iniciar = False

        if beneficio_id:  # <-- Aqui está o correto!
            try:
                beneficio = SeguroDefesoBeneficioModel.objects.get(pk=beneficio_id)
                # Sempre pega todos os controles do benefício!
                associados_beneficiados = ControleBeneficioModel.objects.filter(
                    beneficio=beneficio
                ).select_related('associado')
            except SeguroDefesoBeneficioModel.DoesNotExist:
                beneficio = None

            if beneficio:
                ultima_rodada = ControleBeneficioModel.objects.filter(
                    beneficio=beneficio
                ).aggregate(Max('rodada'))['rodada__max'] or 1

                total_controles = ControleBeneficioModel.objects.filter(
                    beneficio=beneficio,
                    rodada=ultima_rodada
                ).count()

                total_processados = ControleBeneficioModel.objects.filter(
                    beneficio=beneficio,
                    rodada=ultima_rodada,
                    processada=True
                ).count()

                print('==== DEBUG ====')  # Pode ver isso no terminal
                print(f"Rodada: {ultima_rodada} - Total: {total_controles} - Processados: {total_processados}")

                mostrar_reset = (total_controles > 0) and (total_processados == total_controles)
                mostrar_iniciar = (total_controles > 0) and (total_processados < total_controles)

        return render(request, self.template_name, {
            'beneficios': beneficios,
            'beneficio_id': beneficio_id,
            'beneficio': beneficio,
            'associados_beneficiados': associados_beneficiados,
            'mostrar_reset': mostrar_reset,
            'mostrar_iniciar': mostrar_iniciar,
        })

        

class ControleBeneficioEditView(UpdateView):
    model = ControleBeneficioModel
    form_class = ControleBeneficioForm
    template_name = 'defeso/controle_beneficio_edit.html'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.processada = True
        self.object.em_processamento_por = None
        self.object.save()

        action = self.request.POST.get('action', 'salvar')
        if action == 'salvar_proximo':
            # Buscar o próximo controle (do fluxo)
            next_controle = self.get_next_controle(self.object)
            if next_controle:
                next_controle.em_processamento_por = self.request.user
                next_controle.save(update_fields=['em_processamento_por'])
                return redirect('app_defeso:controle_beneficio_edit', pk=next_controle.pk)
            else:
                messages.success(self.request, "Todos os controles deste benefício foram processados!")
                return redirect('app_defeso:lancamento_defeso')
        else:
            # Só salva e fica na mesma página (feedback para usuário)
            messages.success(self.request, "Alterações salvas!")
            return super().form_valid(form)

    def get_next_controle(self, current_controle):
        return ControleBeneficioModel.objects.filter(
            beneficio=current_controle.beneficio,
            rodada=current_controle.rodada,
            processada=False,
            em_processamento_por__isnull=True
        ).exclude(pk=current_controle.pk).order_by('id').first()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        controle = self.object
        associado = controle.associado

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
            '0010_CTPS_Cart_Trabalho', 
            '0011_Declaração_Residência_MAPA',  
            '0012_Ficha_Req_Filiação_ASS_PRESID_JUR', 
            '0013_Ficha_Req_Filiação_ASS_Associado',  
            '0014_Foto_3x4', 
            '0015_Licença_Embarcação',  
            '0016_NIT_Extrato',  
            '0017_Procuração_AD_JUDICIA',  
            '0018_Procuracao_ADMINISTRATIVA',  
            '0019_Protocolo_ENTRADA_RGP',  
            '0020_RG_Identidade_CIN',
            '0021_RGP_Cart_Pescador',
            '0021_TIE_Titulo_Embarcação',
            '0022_Titulo_Eleitor',
        ]

        documentos_up = UploadsDocs.objects.filter(
            proprietario_object_id=associado.pk,
            proprietario_content_type=ContentType.objects.get_for_model(type(associado)),
            tipo__nome__in=tipos_doc_essencial
        ).select_related('tipo')
        context['documentos_essenciais_up'] = documentos_up
        # ---------- PAINEL DE PROCESSAMENTO -------------
        # Total de controles da rodada/benefício atual
        total_controles = ControleBeneficioModel.objects.filter(
            beneficio=controle.beneficio,
            rodada=controle.rodada
        ).count()

        # Pegando todos os controles ordenados para saber o índice do atual
        controles_ordenados = list(ControleBeneficioModel.objects.filter(
            beneficio=controle.beneficio,
            rodada=controle.rodada
        ).order_by('id'))  # ou por nome, etc

        try:
            controle_index = controles_ordenados.index(controle) + 1  # 1-based
        except ValueError:
            controle_index = '?'

        # Usuários atualmente processando
        usuarios_em_processamento = ControleBeneficioModel.objects.filter(
            beneficio=controle.beneficio,
            rodada=controle.rodada,
            em_processamento_por__isnull=False
        ).exclude(pk=controle.pk).values_list('em_processamento_por__username', flat=True).distinct()

        context.update({
            'controle': controle,
            'beneficio': controle.beneficio,
            'rodada': controle.rodada,
            'controle_index': controle_index,
            'total_controles': total_controles,
            'usuarios_em_processamento': usuarios_em_processamento,
        })
        # Novo: flag para mostrar botão "Salvar e Próximo"
        pode_salvar_proximo = (
            controle.em_processamento_por and
            self.request.user == controle.em_processamento_por
        )

        context['pode_salvar_proximo'] = pode_salvar_proximo        
        return context
    
    def get_success_url(self):
        return reverse_lazy('app_defeso:lancamento_defeso')


def proximo_controle_para_processar(request):
    beneficio_id = request.GET.get('beneficio_id')
    if not beneficio_id or not beneficio_id.isdigit():
        messages.error(request, "Benefício não selecionado.")
        return redirect('app_defeso:lancamento_defeso')
    beneficio = get_object_or_404(SeguroDefesoBeneficioModel, pk=beneficio_id)
    rodada = ControleBeneficioModel.objects.filter(beneficio=beneficio).aggregate(Max('rodada'))['rodada__max'] or 1
    controle = pegar_proximo_defeso_para_usuario(beneficio, rodada, request.user)
    if controle:
        return redirect('app_defeso:controle_beneficio_edit', pk=controle.pk)
    else:
        messages.success(request, "Todos os controles já foram processados para este benefício!")
        return redirect('app_defeso:lancamento_defeso')

@require_POST
@login_required
def resetar_rodada_processamento(request):
    beneficio_id = request.POST.get('beneficio_id')
    beneficio = get_object_or_404(SeguroDefesoBeneficioModel, pk=beneficio_id)
    ultima_rodada = ControleBeneficioModel.objects.filter(
        beneficio=beneficio
    ).aggregate(Max('rodada'))['rodada__max'] or 1
    qs = ControleBeneficioModel.objects.filter(
        beneficio=beneficio, rodada=ultima_rodada
    )
    qs.update(processada=False, em_processamento_por=None)
    messages.success(request, f"Rodada {ultima_rodada} resetada!")
    return redirect(f"{reverse('app_defeso:lancamento_defeso')}?beneficio={beneficio.id}")
