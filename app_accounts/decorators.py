# app_accounts/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin



def group_required(*group_names):
    """Verifica se o usuário pertence a um dos grupos informados"""
    def in_groups(u):
        if u.is_authenticated:
            if u.groups.filter(name__in=group_names).exists() or u.is_superuser:
                return True
        raise PermissionDenied
    return user_passes_test(in_groups)



class SuperuserOrAdminGeralRequiredMixin(UserPassesTestMixin):
    login_url = '/accounts/login/'  # ou use reverse_lazy('account_login')

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='admin_geral').exists()
