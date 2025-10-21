# app_accounts/mixins.py

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None  # string ou lista
    login_url = '/accounts/login/'  # URL de fallback

    def test_func(self):
        user = self.request.user
        required = self.group_required

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if isinstance(required, str):
            required = [required]

        return user.groups.filter(name__in=required).exists()

    def handle_no_permission(self):
        user = self.request.user

        if not user.is_authenticated:
            return super().handle_no_permission()

        # ✅ Mensagem amigável + redirecionamento
        messages.error(
            self.request,
            "Você não tem permissão para acessar esta página. "
            "Entre em contato com o administrador do sistema."
        )
        return redirect('app_home:home')

