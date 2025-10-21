# app_accounts/manegement/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app_accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Cria os grupos de usuários iniciais e suas permissões'
    
    def handle(self, *args, **options):
        # Grupo de Administradores Gerais de cada Associaão
        admin_group, created = Group.objects.get_or_create(name='admin_associacao')

        # Grupo de Diretores
        diretor_group, created = Group.objects.get_or_create(name='diretor')
        
        # Grupo de Presidentes
        presidente_group, created = Group.objects.get_or_create(name='presidente')

        # Grupo de Delegados
        delagado_group, created = Group.objects.get_or_create(name='delagado')
                        
        # Grupo de Financeiro - Geral
        financeiro_group, created = Group.objects.get_or_create(name='financeiro')
  
        # Grupo de Recursdos humanaos -  Geral 
        recursos_humanos_group, created = Group.objects.get_or_create(name='recursos_humanos')
        
        # Grupo de Auxiliares das Associações
        auxiliar_associacao, created = Group.objects.get_or_create(name='auxiliar_associacao')

        # Grupo de de Auxiliares das Repartições
        auxiliar_reparticao, created = Group.objects.get_or_create(name='auxiliar_reparticao')        
                           
        # Grupo de Auxiliares Estras
        auxiliar_extra_group, created = Group.objects.get_or_create(name='auxiliar_extra')
        
        # Grupo de Clientes Vip
        cliente_vip_group, created = Group.objects.get_or_create(name='cliente_vip')

        # Grupo de Clientes
        cliente_group, created = Group.objects.get_or_create(name='cliente')
        
        # Grupo de Clientes
        associado_group, created = Group.objects.get_or_create(name='associado')
                
        self.stdout.write(self.style.SUCCESS('Grupos criados com sucesso!'))