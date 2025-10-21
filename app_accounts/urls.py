from django.urls import path
from . import views
from allauth.account.views import LoginView, LogoutView

app_name = 'app_accounts'

urlpatterns = [
    path('dashboards/', views.dashboard, name='dashboard_superuser'),
    path('dashboards/', views.dashboard, name='admin_geral'),
    path('dashboards/', views.dashboard, name='auxiliar_associacao'),

    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    
    path('acesso-negado/', views.AcessoNegadoView.as_view(), name='unauthorized'),
    
    #Criar Usser Fake
    path('criar-fake/', views.criar_usuario_fake, name='criar_usuario_fake'),
    path('inserir-usuario-grupo/', views.InsertUserGroupView.as_view(), name='insert_user_group'),
]
