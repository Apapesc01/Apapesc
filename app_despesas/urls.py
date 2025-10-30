
from django.urls import path
from . import views

# App Space Name
app_name = 'app_despesas'

urlpatterns = [
    path('create/', views.CreateDespesaView.as_view(), name='create_despesa'),
    path('lista/', views.ListDespesasView.as_view(), name='list_despesas'),
    path('editar/<int:pk>/', views.EditDespesasView.as_view(), name='edit_despesa'),
]