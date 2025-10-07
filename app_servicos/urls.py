from django.urls import path
from . import views

# App Space Name
app_name = 'app_servicos'

urlpatterns = [

    path('servico/create/<int:associado_id>/', views.ServicoCreateView.as_view(), name='create_servico'),
    path('servico/detalhes/<int:pk>/', views.ServicoSingleView.as_view(), name='single_servico'),
    path('servico/editar/<int:pk>/', views.ServicoUpdateView.as_view(), name='edit_servico'),
    path('servico/lista/', views.ServicoListView.as_view(), name='list_servicos'),
    path('entrada/create/<int:servico_id>/', views.EntradaCreateView.as_view(), name='create_entrada'),
    path('entrada/edit/<int:pk>/', views.EditarEntradaView.as_view(), name='edit_entrada'),
    path('registrar/pagamento/<int:servico_id>/', views.RegistrarPagamentoEntradaView.as_view(), name='registrar_pagamento_entrada'),

   
]
