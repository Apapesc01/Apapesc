from django.core.management.base import BaseCommand
from app_uploads.models import TipoDocumentoUp

TIPOS_DOCS = [
    ("001_Autodeclaracao_Pesca", "Auto declaração para pescadores."),
    ("002_Autorizacao_Acesso_GOV", "Autorização de acesso ao GOV do associado."),
    ("003_Autorizacao_Imagem", "Autorização de uso de imagem do associado."),
    ("004_CAEPF", "Documento CAEPF do associado."),
    ("005_CEI", "Cadastro Específico do INSS (CEI)."),
    ("006_CNH", "Carteira Nacional de Habilitação."),
    ("007_Comprovante_Residencia", "Comprovante de residência: luz, água, faturas."),
    ("008_Comprovante_Seguro_Defeso", "Comprovante de Seguro Defeso."),
    ("009_CPF", "CPF do associado."),
    ("010_CTPS", "Carteira de Trabalho e Previdência Social."),
    ("011_Declaracao_Residencia_MAPA", "Declaração de residência para o MAPA."),
    ("012_Declaracao_Veracidade", "Declaração de Veracidade."),
    ("013_Ficha_Filiacao", "Ficha de filiação do associado."),
    ("014_Foto_3x4", "Foto 3x4 do associado."),
    ("015_Licenca_Embarcacao", "Licença de embarcação."),
    ("016_NIT_Extrato", "Extrato do Número de Identificação do Trabalhador."),
    ("017_Procuracao_Judicial", "Procuração para advogado/judicial."),
    ("018_Procuracao_Administrativa", "Procuração administrativa."),
    ("019_Protocolo_Entrada_RGP", "Protocolo de entrada do RGP."),
    ("020_RG_Antigo", "RG Antigo."),
    ("021_RG_CIN", "RG (Carteira de Identidade Nacional)."),
    ("022_RGP", "Carteira RGP do pescador."),
    ("023_POP", "Carteira POP do pescador."),
    ("024_TIE", "Título de Embarcação (TIE)."),
    ("025_Titulo_Eleitor", "Título de Eleitor do associado."),
]

class Command(BaseCommand):
    help = 'Cria todos os tipos de documento essenciais para uploads'

    def handle(self, *args, **options):
        count = 0
        for nome, descricao in TIPOS_DOCS:
            obj, created = TipoDocumentoUp.objects.get_or_create(
                nome=nome,
                defaults={"descricao": descricao}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔️ Tipo criado: {nome}"))
                count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Já existia: {nome}"))
        self.stdout.write(self.style.SUCCESS(f"\nTotal de tipos criados: {count}"))
