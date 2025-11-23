from django.core.management.base import BaseCommand
from app_uploads.models import TipoDocumentoUp

TIPOS_DOCS = [
    ("001_Autodeclaracao_Pesca", "Auto declaração para pescadores."),
    ("002_Autorizacao_Acesso_GOV_ASS_associado", "Autorização de acesso ao GOV do associado."),
    ("003_Autorizacao_Imagem_ASS_associado", "Autorização de uso de imagem do associado."),
    ("004_CAEPF", "Documento CAEPF do associado."),
    ("005_CEI", "Cadastro Específico do INSS (CEI)."),
    ("006_CIN_Marinha", "Carteira Marinha (CIN)."),
    ("007_CNH", "Carteira Nacional de Habilitação."),
    ("008_Comprovante_Residencia", "Comprovante de residência: luz, água, faturas."),
    ("009_Comprovante_Seguro_Defeso", "Comprovante de Seguro Defeso."),
    ("010_CPF", "CPF do associado."),
    ("011_CTPS", "Carteira de Trabalho e Previdência Social."),
    ("012_Declaracao_Residencia_MAPA", "Declaração de residência para o MAPA."),
    ("013_Declaracao_Residencia", "Declaração de residência."),
    ("014_Declaracao_Veracidade_ASS_associado", "Declaração de Veracidade Assinada."),
    ("015_Declaracao_Hipo_ASS_associado", "Declaração de Hiposuficiência Assinada."),
    ("016_Declaracao_Filiacao_ASS_Jur", "Declaração de Filiação Assinada."),
    ("017_Declaracao_Ativ_Pesqueira_ASS_Jur", "Declaração de Ativ. Pesqueira Assinada."),
    ("018_Ficha_Prod_Anual_reap_ASS_associado", "Ficha de Produção Anual do associado (REAP)."),
    ("019_Ficha_Requer_Filiacao_ASS_associado", "Ficha de Requerimento de Filiação assinada pelo associado."),
    ("020_Foto_3x4", "Foto 3x4 do associado."),
    ("021_Licenca_Embarcacao", "Licença de embarcação."),
    ("022_NIT_Extrato", "Extrato do Número de Identificação do Trabalhador."),
    ("023_Procuracao_Judicial", "Procuração para advogado/judicial."),
    ("024_Procuracao_Administrativa", "Procuração administrativa."),
    ("025_Protocolo_Entrada_RGP", "Protocolo de entrada do RGP."),
    ("026_RG_Antigo", "RG Antigo."),
    ("027_RG_CIN", "RG (Carteira de Identidade Nacional)."),
    ("028_RGP", "Carteira RGP do pescador."),
    ("029_POP", "Carteira POP do pescador."),
    ("030_TIE", "Título de Embarcação (TIE)."),
    ("031_Titulo_Eleitor", "Título de Eleitor do associado."),
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
