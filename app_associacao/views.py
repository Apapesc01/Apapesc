# Views - App Associacao
from core.views.base_imports import *
from core.views.app_associacao_imports import *



# LISTA E EDIÇÂO DE USUÀRIOS ========================================
class UserListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    template_name = 'associacao/list_users.html'
    context_object_name = 'users'
    ordering = ['username', '-date_joined']
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
        queryset = super().get_queryset().select_related(
            'integrante__reparticao',
            'integrante__cargo'
        ).prefetch_related('associado')
        return queryset

        
class UserUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'associacao/edit_user.html'
    success_url = reverse_lazy('app_associacao:list_users')
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
        action = self.request.POST.get('action')  # Verifica qual botão foi clicado
        response = super().form_valid(form)

        if action == 'save_and_integrante':
            # Redireciona para a criação do integrante
            return redirect(reverse('app_associacao:create_integrante') + f'?user_id={self.object.id}')
        
        if action == 'save_and_associado':
            # Verifica se o usuário já é um associado
            if AssociadoModel.objects.filter(user=self.object).exists():
                messages.error(self.request, "Este usuário já é um associado!")
                return redirect(self.success_url)  # Redireciona para a lista de usuários

            # Redireciona para a criação de associado
            return redirect(reverse('app_associados:create_associado') + f'?user_id={self.object.id}')
        
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        context['is_associado'] = hasattr(user, 'associado')
        context['is_integrante'] = hasattr(user, 'integrante')

        return context

   
# ----------------------------------------------------------    


# CREATES ==========================================
class AssociacaoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = AssociacaoModel
    form_class = AssociacaoForm
    template_name = 'associacao/create_associacao.html'
    group_required = [
        'Superuser',
    ]        

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            messages.error(request, "Você não tem permissão para criar uma associação.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        messages.success(self.request, 'Associação criada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar a Associação. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('app_associacao:single_associacao', kwargs={'pk': self.object.pk})

        
class ReparticaoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = ReparticoesModel
    form_class = ReparticoesForm
    template_name = 'associacao/create_reparticao.html'
    success_url = reverse_lazy('app_associacao:list_reparticoes')
    extra_context = {'titulo_pagina': 'Nova Repartição'}
    group_required = [
        'Superuser',
    ]    
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            messages.error(request, "Você não tem permissão para criar uma associação.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Repartição criada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar a Repartição. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('app_associacao:single_reparticao', kwargs={'pk': self.object.pk})

class IntegranteCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = IntegrantesModel
    form_class = IntegrantesForm
    template_name = 'associacao/create_integrante.html'
    success_url = reverse_lazy('app_associacao:list_integrantes')
    group_required = [
        'Superuser',
        'admin_associacao',

    ]    
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and (request.user.is_superuser or request.user.user_type == 'admin_associacao')):
            messages.error(self.request, "Você não tem permissão para visualizar essa Página.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)  
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.GET.get('user_id') or None
        associacao_id = self.request.GET.get('associacao_id') or None

        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            kwargs['user_initial'] = user

        if associacao_id:
            kwargs['associacao_id'] = associacao_id

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
        user_id = self.request.GET.get('user_id')
        if user_id:
            form.instance.user = get_object_or_404(CustomUser, pk=user_id)

        # Verifica se o campo de 'reparticao' está vazio ou None, e trata a atribuição
        if 'reparticao' in form.cleaned_data and form.cleaned_data['reparticao'] is None:
            form.instance.reparticao = None  # Ou pode definir um valor padrão, se necessário

        messages.success(self.request, 'Integrante criado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar a Integrante. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('app_associacao:single_integrante', kwargs={'pk': self.object.pk})   
    
    
class MunicipioCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = MunicipiosModel
    form_class = MunicipiosForm
    template_name = 'associacao/create_municipio.html'
    success_url = reverse_lazy('app_associacao:list_municipios') 
    extra_context = {'titulo_pagina': 'Novo Município'} 
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
        messages.success(self.request, 'Município criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar a município. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)
    

class ProfissaoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = ProfissoesModel
    form_class = ProfissoesForm
    template_name = 'associacao/create_profissao.html'
    success_url = reverse_lazy('app_associacao:list_profissoes') 
    extra_context = {'titulo_pagina': 'Nova Profissão'}
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
        messages.success(self.request, 'Profissão criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar a Profissão. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)
        
                
class CargosCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = CargosModel
    form_class = CargosForm
    template_name = 'associacao/create_cargo.html'
    success_url = reverse_lazy('app_associacao:list_cargos') 
    extra_context = {'titulo_pagina': 'Novo Cargo'} 
    group_required = [
        'Superuser',
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
        messages.success(self.request, 'Cargo criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar a Cargo. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)
        
# ----------------------------------------------------


# LISTS ==========================================    
class AssociacaoListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = AssociacaoModel
    template_name = 'associacao/list_associacoes.html'
    context_object_name = 'associacoes'
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


class ReparticoesListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = ReparticoesModel
    template_name = 'associacao/list_reparticoes.html'
    context_object_name = 'reparticoes'
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
    
    
class IntegrantesListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = IntegrantesModel
    template_name = 'associacao/list_integrantes.html'
    context_object_name = 'integrantes'
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
    
        
class MunicipiosListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = MunicipiosModel
    template_name = 'associacao/list_municipios.html'
    context_object_name = 'municipios'
    ordering = ['municipio']
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
    
    
class ProfissoesListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = ProfissoesModel
    template_name = 'associacao/list_profissoes.html'
    context_object_name = 'profissoes'
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
    
    
class CargosListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CargosModel
    template_name = 'associacao/list_cargos.html'
    context_object_name = 'cargos'
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
# ----------------------------------------------------


# EDITS ==========================================                    
class AssociacaoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = AssociacaoModel
    form_class = AssociacaoForm
    template_name = 'associacao/edit_associacao.html'
    success_url = reverse_lazy('app_associacao:list_associacoes')
    group_required = [
        'Superuser',
    ]    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            messages.error(request, "Você não tem permissão para criar uma associação.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs) 
    
    def form_valid(self, form):
        messages.success(self.request, 'Associação atualizada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar a associação. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)    

    def get_success_url(self):
        return reverse_lazy('app_associacao:single_associacao', kwargs={'pk': self.object.pk})


class ReparticaoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = ReparticoesModel
    form_class = ReparticoesForm
    template_name = 'associacao/edit_reparticao.html'
    group_required = [
        'Superuser',
    ]    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            messages.error(request, "Você não tem permissão para criar uma associação.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Associação atualizada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar a associação. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)  
        
    def get_success_url(self):
        return reverse_lazy('app_associacao:single_reparticao', kwargs={'pk': self.object.pk})

    
class MunicipioUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = MunicipiosModel
    form_class = MunicipiosForm
    template_name = 'associacao/edit_municipio.html'
    success_url = reverse_lazy('app_associacao:list_municipios') 
    extra_context = {'titulo_pagina': 'Editar Município'}    
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
        messages.success(self.request, 'Município atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao altualizar a município. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)    


class CargoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = CargosModel
    form_class = CargosForm
    template_name = 'associacao/edit_cargo.html'
    success_url = reverse_lazy('app_associacao:list_cargos') 
    extra_context = {'titulo_pagina': 'Editar Cargo'} 
    group_required = [
        'Superuser',
    ]    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            messages.error(request, "Você não tem permissão para criar uma associação.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Cargo atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar o cargo. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)   
    
    
class ProfissaoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = ProfissoesModel
    form_class = ProfissoesForm
    template_name = 'associacao/edit_profissao.html'
    success_url = reverse_lazy('app_associacao:list_profissoes') 
    extra_context = {'titulo_pagina': 'Editar Profissão'} 
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
        messages.success(self.request, 'Profissão atualizada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar a profissão. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)     
    
    
class IntegranteUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = IntegrantesModel
    form_class = IntegrantesForm
    template_name = 'associacao/edit_integrante.html'
    group_required = [
        'Superuser',
        'admin_associacao',
    ]    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and (request.user.is_superuser or request.user.user_type == 'admin_associacao')):
            messages.error(self.request, "Você não tem permissão para visualizar essa Página.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)  
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.GET.get('user_id') or None
        associacao_id = self.request.GET.get('associacao_id') or None

        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            kwargs['user_initial'] = user

        if associacao_id:
            kwargs['associacao_id'] = associacao_id

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
        user_id = self.request.GET.get('user_id')
        if user_id:
            form.instance.user = get_object_or_404(CustomUser, pk=user_id)


        user_type = form.cleaned_data['user_type']
        form.instance.user.user_type = user_type
        form.instance.user.save()  # Salva as alterações no usuário

        # Salva a relação Many-to-Many (se houver algum grupo selecionado)
        group = form.cleaned_data['group']
        form.instance.user.groups.set([group])  # Atualiza a relação Many-to-Many

        # Verifica se o campo de 'reparticao' está vazio ou None, e trata a atribuição
        if 'reparticao' in form.cleaned_data and form.cleaned_data['reparticao'] is None:
            form.instance.reparticao = None  # Ou pode definir um valor padrão, se necessário

        messages.success(self.request, 'Integrante atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar o Integrante. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('app_associacao:single_integrante', kwargs={'pk': self.object.pk})    
# ----------------------------------------------------


# SINGLES ==========================================  
class AssociacaoDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = AssociacaoModel
    template_name = 'associacao/single_associacao.html'
    context_object_name = 'associacao'
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
        context['titulo_pagina'] = 'Detalhes da Associação'
        return context    
    
class ReparticaoDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = ReparticoesModel
    template_name = 'associacao/single_reparticao.html'
    context_object_name = 'reparticao'
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
        context['titulo_pagina'] = 'Detalhes da Repartição'
        return context

class IntegranteDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = IntegrantesModel
    template_name = 'associacao/single_integrante.html'
    context_object_name = 'integrante'
    group_required = [
        'Superuser',
        'admin_associacao',
    ]    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and (request.user.is_superuser or request.user.user_type == 'admin_associacao')):
            messages.error(self.request, "Você não tem permissão para visualizar essa Página.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)  
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Detalhes do Integrante'
        return context    
# ----------------------------------------------------    

# FUNCÇÕES
def reparticoes_por_associacao(request):
    associacao_id = request.GET.get('associacao_id')
    data = []

    if associacao_id:
        # Filtra as repartições pela associação selecionada
        reparticoes = ReparticoesModel.objects.filter(associacao_id=associacao_id)

        # Garante que as repartições não serão duplicadas
        data = [{'id': rep.id, 'nome': rep.nome_reparticao} for rep in reparticoes]

    return JsonResponse({'reparticoes': data})

def municipios_por_reparticao(request):
    reparticao_id = request.GET.get('reparticao_id')
    municipios = []

    if reparticao_id:
        try:
            reparticao = ReparticoesModel.objects.get(pk=reparticao_id)
            municipios_qs = reparticao.municipios_circunscricao.all()
            municipios = [{'id': m.id, 'nome': m.municipio} for m in municipios_qs]
        except ReparticoesModel.DoesNotExist:
            pass

    return JsonResponse({'municipios': municipios})