from core.views.base_imports import *
from core.views.app_graficos_imports import *

class GraficosSuperView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'graficos/graficos_superuser.html'
    group_required = ['Superuser']
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        context = {}  # você pode passar dados aqui
        return render(request, self.template_name, context)



