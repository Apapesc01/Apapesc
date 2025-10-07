
from app_servicos.models import ServicoModel, EntradaFinanceiraModel, PagamentoEntrada

from app_servicos.forms import ServicoForm, PagamentoEntradaForm, EntradaFinanceiraForm

from app_associados.models import AssociadoModel

from core.choices import (
    STATUS_COBRANCA,
    STATUS_PAGAMENTO_CHOICES,
    FORMA_PAGAMENTO_CHOICES,
    PARCELAMENTO_CHOICES,
    TIPO_SERVICO,
    NATUREZA_SERVICO_CHOICES,
    STATUS_EMISSAO_DOC,
    STATUS_CONSULTORIA,
    STATUS_ASSESSORIA_PROCESSO
    )

from app_uploads.models import UploadsDocs