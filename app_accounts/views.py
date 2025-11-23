# app_accounts
from core.views.base_imports import *
from core.views.app_accounts_imports import *

@login_required
def dashboard(request):
    user = request.user

    if user.is_superuser:
        # Redireciona para a view que tem o contexto!
        return redirect('app_dashboards:super_dashboard')
    
    user_type_template_map = {
        'admin_associacao': 'dashboard_admin.html',
        'diretor': 'dashboard_diretor.html',
        'presidente': 'dashboard_presidente.html',
        'delagado': 'dashboard_deleagdo.html',
        'financeiro': 'dashboard_financeiro.html',
        'recursos_humanos': 'dashboard_recursos_humanos.html',
        'auxiliar_associacao': 'dashboard_aux_associacao.html',
        'auxiliar_reparticao': 'dashboard_aux_reparticao.html',
        'auxiliar_extra': 'dashboard_aux_extra.html',
        'cliente_vip': 'dashboard_cliente_vip.html',
        'cliente': 'dashboard_cliente.html',
        'associado':'dashboard_associado',
    }

    template = user_type_template_map.get(user.user_type, 'dashboard_cliente.html')
    return render(request, f'dashboards/{template}')

class AcessoNegadoView(TemplateView):
    template_name = 'account/acesso_negado.html'


User = get_user_model()

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'admin_associacao' or u.user_type == 'auxiliar_associacao')
def criar_usuario_fake(request):
    try:
        prefix = "0000FAKE"
        base_username = "0000fake"
        base_email = "@email.com"
        password = "@senhafake"
        user_type_default = "cliente"

        # Busca maior número usado
        existing_fakes = User.objects.filter(username__startswith=base_username)
        next_number = 1

        if existing_fakes.exists():
            ultimos_numeros = [
                int(u.username.replace(base_username, '').replace('User_fake', '')) 
                for u in existing_fakes if u.username.replace(base_username, '').replace('User_fake', '').isdigit()
            ]
            next_number = max(ultimos_numeros) + 1 if ultimos_numeros else 1

        # Formata número
        numero_formatado = f"{next_number:04d}"

        # Cria campos
        username = f"{base_username}{numero_formatado}"
        email = f"{prefix}{numero_formatado}{base_email}"

        # Cria usuário
        novo_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type=user_type_default
        )

        messages.success(request, f"✅ Usuário fake criado: {username} / {email}")
        return redirect('app_associacao:list_users')

    except Exception as e:
        print("❌ Erro ao criar usuário fake:", str(e))
        traceback.print_exc()
        messages.error(request, "Erro interno ao criar usuário fake. Consulte os logs.")
        return redirect('app_associacao:list_users')  



class InsertUserGroupView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'account/insert_user_group.html'
    group_required = [
    'Superuser', # Somente Superusuário tem permissão para inserir INTEGRANTE à um grupo. OBS, o type também deve corresponder ao super usuário.
    ]   
    
    
    def dispatch(self, request, *args, **kwargs):
        # Verifica se o usuário tem permissão para criar um associado
        if not (request.user.is_authenticated and (request.user.is_superuser or request.user.user_type == 'auxiliar_associacao' or request.user.user_type == 'admin_associacao')):
            messages.error(self.request, "Você não tem permissão para Editar um associado.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)  
    
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Você não tem permissão para acessar esta página.")
        return redirect('app_home:home')  # ajuste conforme sua home

    
    def get(self, request):
        search_query = request.GET.get('q', '').strip()

        users = User.objects.all().order_by('username')
        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

        groups = Group.objects.all().order_by('name')
        return render(request, self.template_name, {
            'users': users,
            'groups': groups,
            'search_query': search_query,
        })


    def post(self, request):
        user_id = request.POST.get('user_id')
        group_name = request.POST.get('group_name')

        user = User.objects.filter(id=user_id).first()
        group = Group.objects.filter(name=group_name).first()

        if not user or not group:
            messages.error(request, "Usuário ou grupo inválido.")
        else:
            user.groups.clear()
            user.groups.add(group)
            messages.success(request, f"Grupo atualizado para {user.get_full_name() or user.username}.")

        return redirect('app_accounts:insert_user_group')