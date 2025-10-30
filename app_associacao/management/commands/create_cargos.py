# app_associados/management/commands/create_cargos.py

from django.core.management.base import BaseCommand
from app_associacao.models import CargosModel  # ajuste se o nome do model for diferente


CARGOS = [
    "Administrador(a) da Associação",
    "Advogada",
    "Advogado",
    "Auxiliar da Associação",
    "Auxiliar Extra",
    "Auxiliar Manutenção",
    "Auxiliar Repartição",
    "Carpinteiro",
    "Cozinheiro(a)",
    "Delegado(a) Repartição",
    "Diretor",
    "Financeiro",
    "Motorista",
    "Presidente",
    "RH",
]


class Command(BaseCommand):
    help = 'Cria as Cargos padrão no banco de dados'

    def handle(self, *args, **options):
        count = 0
        for nome in sorted(CARGOS):
            obj, created = CargosModel.objects.get_or_create(nome=nome)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔️ Cargo criada: {nome}"))
                count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Já existia: {nome}"))
        self.stdout.write(self.style.SUCCESS(f"\nTotal de cargos criadas: {count}"))