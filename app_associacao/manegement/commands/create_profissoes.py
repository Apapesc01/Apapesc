# app_associados/management/commands/create_profissoes.py

from django.core.management.base import BaseCommand
from app_associados.models import ProfissoesModel  # ajuste se o nome do model for diferente

PROFISSOES = [
    ("Advogada", "Profissional formada em Direito, atuante na advocacia."),
    ("Advogado", "Profissional formado em Direito, atuante na advocacia."),
    ("Aposentado(a)", "Pessoa aposentada, sem exercício profissional ativo."),
    ("Aposentado(a) Especial", "Aposentado(a) sob regime de atividade especial, como pesca ou mineração."),
    ("Aposentado(a) Por Idade Rural", "Aposentado(a) por idade, vinculado a atividades rurais."),
    ("Aposentado(a) Por Idade Urbana", "Aposentado(a) por idade, vinculado a atividades urbanas."),
    ("Aposentado(a) Por Invalidez", "Aposentado(a) em razão de invalidez."),
    ("Auxiliar de Serviços Gerais", "Profissional que presta apoio em diversas tarefas operacionais."),
    ("Carpinteiro", "Profissional que trabalha com construção e reparos em madeira."),
    ("Cozinheiro(a)", "Profissional responsável pelo preparo de refeições."),
    ("Do Lar", "Pessoa dedicada às atividades domésticas."),
    ("Marinheiro de Convés", "Auxilia nas atividades gerais de bordo."),
    ("Mecânico Naval", "Realiza manutenção de motores e sistemas embarcados."),
    ("Motorista", "Profissional que realiza transporte terrestre de pessoas ou cargas."),
    ("Motorista de Embarcação", "Responsável pela condução da embarcação."),
    ("Médico", "Profissional da área da saúde habilitado a exercer a medicina."),
    ("Pedreiro", "Profissional responsável pela execução de alvenaria e estruturas civis."),
    ("Pescador Profissional", "Atua na pesca artesanal ou industrial."),
    ("Pescadora Profissional", "Atua na pesca artesanal ou industrial."),
    ("Professor(a)", "Profissional da área da educação, responsável pelo ensino."),
    ("Servente de Obras", "Auxilia pedreiros e outros profissionais em construções."),
    ("Servidor Público", "Trabalhador vinculado à administração pública direta ou indireta."),
    ("Técnico de Aquicultura", "Trabalha no cultivo e manejo de organismos aquáticos."),
]

class Command(BaseCommand):
    help = 'Cria as profissões padrão no banco de dados'

    def handle(self, *args, **options):
        count = 0
        for nome, descricao in PROFISSOES:
            obj, created = ProfissoesModel.objects.get_or_create(
                nome=nome,
                defaults={"descricao": descricao}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔️ Profissão criada: {nome}"))
                count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Já existia: {nome}"))
        self.stdout.write(self.style.SUCCESS(f"\nTotal de profissões criadas: {count}"))
