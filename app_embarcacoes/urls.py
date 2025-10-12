from django.urls import path
from . import views

# App Space Name
app_name = 'app_embarcacoes'

urlpatterns = [
    path('nova/<int:associado_id>/', views.CreateEmbarcacaoView.as_view(), name='create_embarcacao'),
    path('embarcacao/<int:pk>/', views.SingleEmbarcacaoView.as_view(), name='single_embarcacao'),
    path('edit-embarcacao/<int:pk>/', views.EditEmbarcacaoView.as_view(), name='edit_embarcacao'),
]
