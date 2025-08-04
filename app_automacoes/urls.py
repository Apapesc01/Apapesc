from django.urls import path
from . import views

# Gerar declarações e carteirinha list documentos uploads app_automaçoes Templates
app_name = 'app_automacoes'

urlpatterns = [
    
     # Uploads
    path('upload/residencia/', views.upload_pdf_base, {'automacao': 'residencia'}, name='upload_pdf_residencia'),
    
    # Lista de todos os arquivos PDF
    path('lista/todos-arquivos/', views.ListaTodosArquivosView.as_view(), name='lista_automacoes'),
    
    # Ações
    path('pagina-acoes/', views.pagina_acoes, name='pagina_acoes'),
    path('pagina-acoes/<int:associado_id>/', views.pagina_acoes, name='pagina_acoes'),
    path('pagina-acoes-entrada/<int:entrada_id>/', views.pagina_acoes, name='pagina_acoes_entrada'),
    
    # Gerar Declarações      
    path('declaracao/residencia/<int:associado_id>/', views.gerar_declaracao_residencia,
         name='gerar_declaracao_residencia'), 
    
]