from  app_defeso.models import (
    SeguroDefesoBeneficioModel,
    ControleBeneficioModel,
    DecretosModel,
    PeriodoDefesoOficial,
    PortariasModel,
    LeiFederalPrevidenciaria,
    Especie,
    InstrucoesNormativasModel,
    pegar_proximo_defeso_para_usuario,
    resetar_processamento_rodada,
    finalizar_processamento_defeso,
    )
from app_defeso.forms import (
    ControleBeneficioForm,
    SeguroDefesoBeneficioForm,
    DecretosForm,
    InstrucoesNormativasForm,
    PeriodoDefesoOficialForm,
    PortariasForm,
    EspeciesForm,
    LeiFederalPrevidenciariaForm
    )

from app_uploads.models import UploadsDocs
from core.choices import STATUS_BENEFICIO_CHOICES, DAR_ENTRADA_DEFESO_CHOICES