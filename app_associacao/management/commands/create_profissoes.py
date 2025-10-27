# app_associados/management/commands/create_profissoes.py

from django.core.management.base import BaseCommand
from app_associacao.models import ProfissoesModel  # ajuste se o nome do model for diferente


PROFISSOES = [
    "Advogada",
    "Advogado",
    "Aposentado(a)",
    "Aposentado(a) Especial",
    "Aposentado(a) Por Idade Rural",
    "Aposentado(a) Por Idade Urbana",
    "Aposentado(a) Por Invalidez",
    "Auxiliar de Serviços Gerais",
    "Carpinteiro",
    "Cozinheiro(a)",
    "Do Lar",
    "Marinheiro de Convés",
    "Mecânico Naval",
    "Motorista",
    "Motorista de Embarcação",
    "Médico",
    "Pedreiro",
    "Pescador Profissional",
    "Pescadora Profissional",
    "Professor(a)",
    "Servente de Obras",
    "Servidor Público",
    "Técnico de Aquicultura",
]

class Command(BaseCommand):
    help = 'Cria as profissões padrão no banco de dados'

    def handle(self, *args, **options):
        count = 0
        for nome in sorted(PROFISSOES):
            obj, created = ProfissoesModel.objects.get_or_create(nome=nome)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔️ Profissão criada: {nome}"))
                count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Já existia: {nome}"))
        self.stdout.write(self.style.SUCCESS(f"\nTotal de profissões criadas: {count}"))