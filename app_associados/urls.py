from django.urls import path
from . import views

# App Space Name
app_name = 'app_associados'

urlpatterns = [
    # Creates
    path('novo-associado/', views.AssociadoCreateView.as_view(), name='create_associado'),
    path('editar-associado/<int:pk>/', views.AssociadoUpdateView.as_view(), name='edit_associado'),
    
    # Edits
    
    # Lists
    path('associados/', views.AssociadoListView.as_view(), name='list_associados'),
    
    # Singles
    path('associado/<int:pk>/', views.AssociadoSingleView.as_view(), name='single_associado'),
    
    # HISTÓRICO
    path('associado/<int:pk>/historico/', views.AssociadoHistoricoView.as_view(), name='historico_associado'),
    
    # Enviar Drive
    path('enviar-para-drive/<uuid:pk>/', views.EnviarParaDriveView.as_view(), name='enviar_para_drive'),
    
    path('refiliar/<int:user_id>/', views.refiliar_associado, name='refiliar_associado'),


]
