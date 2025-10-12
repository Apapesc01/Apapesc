
from core.views.base_imports import *
from core.views.app_embarcacoes_imports import *


class CreateEmbarcacaoView(LoginRequiredMixin, CreateView):
    model = EmbarcacoesModel
    form_class = EmbarcacaoForm
    template_name = 'embarcacoes/create_embarcacao.html'
    group_required = [
        'Superuser',
        'Admin da Associação',
        'Delegado(a) da Repartição',
        'Diretor(a) da Associação',
        'Presidente da Associação',
        'Auxiliar da Associação',
        'Auxiliar da Repartição',
    ]  

    def dispatch(self, request, *args, **kwargs):
        self.associado = get_object_or_404(AssociadoModel, id=kwargs.get('associado_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['proprietario'] = self.associado
        return kwargs

    def form_valid(self, form):
        embarcacao = form.save(commit=False)
        embarcacao.proprietario = self.associado
        embarcacao.save()

        messages.success(self.request, "Embarcação criada com sucesso! 🚤")
        return redirect('app_embarcacoes:single_embarcacao', pk=embarcacao.pk)


    def form_invalid(self, form):
        messages.error(self.request, "Erro ao salvar embarcação. Verifique os campos obrigatórios.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nova Embarcação"
        context['associado'] = self.associado
        return context
    
    
class SingleEmbarcacaoView(LoginRequiredMixin, DetailView):
    model = EmbarcacoesModel
    template_name = 'embarcacoes/single_embarcacao.html'
    context_object_name = 'embarcacao'    
    

class EditEmbarcacaoView(LoginRequiredMixin, UpdateView):
    model = EmbarcacoesModel
    form_class = EmbarcacaoForm
    template_name = 'embarcacoes/edit_embarcacao.html'
    context_object_name = 'embarcacao'

    def form_valid(self, form):
        messages.success(self.request, "Embarcação atualizada com sucesso! ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar embarcação. Verifique os campos obrigatórios.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('app_embarcacoes:single_embarcacao', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Embarcação"
        return context