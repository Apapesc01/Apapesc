from core.views.base_imports import *
from core.views.app_despesas_imports import *

from app_associacao.models import ReparticoesModel



class CreateDespesaView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = DespesaAssociacaoModel
    form_class = DespesaAssociacaoForm
    template_name = 'despesas/create_despesa.html'
    success_url = reverse_lazy('app_despesas:list_despesas')  # ajuste conforme suas rotas
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
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        associacao_id = self.request.GET.get('associacao') or self.request.POST.get('associacao')
        if associacao_id:
            form.fields['reparticao'].queryset = ReparticoesModel.objects.filter(associacao_id=associacao_id)
        else:
            form.fields['reparticao'].queryset = ReparticoesModel.objects.none()

        return form


    def form_valid(self, form):
        form.instance.registrado_por = self.request.user
        form.instance.usuario_atualizacao = self.request.user
        response = super().form_valid(form)

        action = self.request.POST.get('action')

        if action == 'save_and_continue':
            # Redireciona para o mesmo formulário limpo
            messages.success(self.request, "Despesa salva com sucesso! Você pode adicionar outra.")
            return redirect(reverse('app_despesas:create_despesa'))  # ou sua URL nomeada

        messages.success(self.request, "Despesa salva com sucesso!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associacao_id = self.request.GET.get('associacao_id')


        if associacao_id:
            from app_associacao.models import AssociacaoModel
            context['associacao_obj'] = get_object_or_404(AssociacaoModel, pk=associacao_id)
                    
        context['title'] = 'Registrar Nova Despesa'
        return context
    

def carregar_reparticoes_por_associacao(request):
    associacao_id = request.GET.get('associacao_id')
    reparticoes = ReparticoesModel.objects.filter(associacao_id=associacao_id).values('id', 'nome')
    return JsonResponse({'reparticoes': list(reparticoes)})


class EditDespesasView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = DespesaAssociacaoModel
    form_class = DespesaAssociacaoForm
    template_name = 'despesas/edit_despesa.html'
    success_url = reverse_lazy('app_despesas:list_despesas')
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
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Aplica o filtro de repartições com base na associação atual
        associacao_id = self.request.POST.get('associacao') or self.object.associacao_id
        if associacao_id:
            form.fields['reparticao'].queryset = ReparticoesModel.objects.filter(associacao_id=associacao_id)
        else:
            form.fields['reparticao'].queryset = ReparticoesModel.objects.none()

        return form

    def form_valid(self, form):
        # Adiciona o usuário logado como responsável pela edição
        form.instance.usuario_atualizacao = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Despesa'
        return context
    
class ListDespesasView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = DespesaAssociacaoModel
    template_name = 'despesas/list_despesas.html'
    context_object_name = 'despesas'
    paginate_by = 20
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
        queryset = DespesaAssociacaoModel.objects.all()
        self.filtro_form = FiltroDespesasForm(self.request.GET or None)

        if not self.request.user.is_superuser:
            queryset = queryset.filter(associacao__responsaveis=self.request.user)
            self.filtro_form.fields['associacao'].queryset = AssociacaoModel.objects.filter(responsaveis=self.request.user)

        if self.filtro_form.is_valid():
            associacao = self.filtro_form.cleaned_data.get('associacao')
            reparticao = self.filtro_form.cleaned_data.get('reparticao')
            pago = self.filtro_form.cleaned_data.get('pago')

            if associacao:
                queryset = queryset.filter(associacao=associacao)

            if reparticao:
                queryset = queryset.filter(reparticao=reparticao)

            if pago == 'true':
                queryset = queryset.filter(pago=True)
            elif pago == 'false':
                queryset = queryset.filter(pago=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_form'] = self.filtro_form
        return context