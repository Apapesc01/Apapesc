from django.core.management.base import BaseCommand
from app_uploads.models import TipoDocumentoUp

TIPOS_DOCS = [
    ("001_Auto_Declaração_Pesca", "Auto declaração para pescadores."),
    ("002_Autorização_ACESSO_GOV_ASS_Associado", "Autorização de acesso ao GOV do associado."),
    ("003_Autorização_IMAGEM_ASS_Associado", "Autorização de uso de imagem do associado."),
    ("004_CAEPF", "Documento CAEPF do associado."),
    ("005_CEI", "Cadastro Específico do INSS (CEI)."),
    ("006_CNH_Cart_Motorista", "Carteira Nacional de Habilitação."),
    ("007_Comp_Resid_LUZ_AGUA_FATURAS", "Comprovante de residência: luz, água, faturas."),
    ("008_Comp_SEGURO_DEFESO", "Comprovante de Seguro Defeso."),
    ("009_CPF_Pessoa_Física", "CPF do associado."),
    ("010_CTPS_Cart_Trabalho", "Carteira de Trabalho e Previdência Social."),
    ("011_Declaração_Residência_MAPA", "Declaração de residência para o MAPA."),
    ("012_Ficha_Req_Filiação_ASS_PRESID_JUR", "Ficha de filiação assinada pelo presidente ou jurídico."),
    ("013_Ficha_Req_Filiação_ASS_Associado", "Ficha de filiação do associado."),
    ("014_Foto_3x4", "Foto 3x4 do associado."),
    ("015_Licença_Embarcação", "Licença de embarcação."),
    ("016_NIT_Extrato", "Extrato do Número de Identificação do Trabalhador."),
    ("017_Procuração_AD_JUDICIA", "Procuração para advogado/judicial."),
    ("018_Procuracao_ADMINISTRATIVA", "Procuração administrativa."),
    ("019_Protocolo_ENTRADA_RGP", "Protocolo de entrada do RGP."),
    ("020_RG_Identidade_CIN", "RG (Carteira de Identidade Nacional)."),
    ("021_RGP_Cart_Pescador", "Carteira RGP do pescador."),
    ("021_TIE_Titulo_Embarcação", "Título de Embarcação (TIE)."),
    ("022_Titulo_Eleitor", "Título de Eleitor do associado."),
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
