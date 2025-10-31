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



