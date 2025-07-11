UF_CHOICES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
    ('Undefined ', 'Undefined'),
]
EMISSOR_RG_CHOICES = [
    ('SSP/AC', 'SSP/AC'),
    ('SSP/AL', 'SSP/AL'),
    ('SSP/AP', 'SSP/AP'),
    ('SSP/AM', 'SSP/AM'),
    ('SSP/BA', 'SSP/BA'),
    ('SSP/CE', 'SSP/CE'),
    ('SSP/DF', 'SSP/DF'),
    ('SSP/ES', 'SSP/ES'),
    ('SSP/GO', 'SSP/GO'),
    ('SSP/MA', 'SSP/MA'),
    ('SSP/MG', 'SSP/MG'),
    ('SSP/MS', 'SSP/MS'),
    ('SSP/MT', 'SSP/MT'),
    ('SSP/PA', 'SSP/PA'),
    ('SSP/PB', 'SSP/PB'),
    ('SSP/PE', 'SSP/PE'),
    ('SSP/PI', 'SSP/PI'),
    ('SSP/RJ', 'SSP/RJ'),
    ('SSP/RN', 'SSP/RN'),
    ('SSP/RS', 'SSP/RS'),
    ('SSP/RO', 'SSP/RO'),
    ('SSP/RR', 'SSP/RR'),
    ('SSP/SC', 'SSP/SC'),
    ('SSP/SP', 'SSP/SP'),
    ('SSP/SE', 'SSP/SE'),
    ('SSP/TO', 'SSP/TO'),
    ('UF', 'UF'),
    ('Undefined ', 'Undefined'),
]
EMISSOR_CNH_CHOICES = [
    ('SSP/AC', 'SSP/AC'),
    ('SSP/AL', 'SSP/AL'),
    ('SSP/AP', 'SSP/AP'),
    ('SSP/AM', 'SSP/AM'),
    ('SSP/BA', 'SSP/BA'),
    ('SSP/CE', 'SSP/CE'),
    ('SSP/DF', 'SSP/DF'),
    ('SSP/ES', 'SSP/ES'),
    ('SSP/GO', 'SSP/GO'),
    ('SSP/MA', 'SSP/MA'),
    ('SSP/MG', 'SSP/MG'),
    ('SSP/MS', 'SSP/MS'),
    ('SSP/MT', 'SSP/MT'),
    ('SSP/PA', 'SSP/PA'),
    ('SSP/PB', 'SSP/PB'),
    ('SSP/PE', 'SSP/PE'),
    ('SSP/PI', 'SSP/PI'),
    ('SSP/RJ', 'SSP/RJ'),
    ('SSP/RN', 'SSP/RN'),
    ('SSP/RS', 'SSP/RS'),
    ('SSP/RO', 'SSP/RO'),
    ('SSP/RR', 'SSP/RR'),
    ('SSP/SC', 'SSP/SC'),
    ('SSP/SP', 'SSP/SP'),
    ('SSP/SE', 'SSP/SE'),
    ('SSP/TO', 'SSP/TO'),
    ('UF', 'UF'),
    ('Undefined ', 'Undefined'),
]
EMISSOR_CPTS_CHOICES = [
    ('SSP/AC', 'SSP/AC'),
    ('SSP/AL', 'SSP/AL'),
    ('SSP/AP', 'SSP/AP'),
    ('SSP/AM', 'SSP/AM'),
    ('SSP/BA', 'SSP/BA'),
    ('SSP/CE', 'SSP/CE'),
    ('SSP/DF', 'SSP/DF'),
    ('SSP/ES', 'SSP/ES'),
    ('SSP/GO', 'SSP/GO'),
    ('SSP/MA', 'SSP/MA'),
    ('SSP/MG', 'SSP/MG'),
    ('SSP/MS', 'SSP/MS'),
    ('SSP/MT', 'SSP/MT'),
    ('SSP/PA', 'SSP/PA'),
    ('SSP/PB', 'SSP/PB'),
    ('SSP/PE', 'SSP/PE'),
    ('SSP/PI', 'SSP/PI'),
    ('SSP/RJ', 'SSP/RJ'),
    ('SSP/RN', 'SSP/RN'),
    ('SSP/RS', 'SSP/RS'),
    ('SSP/RO', 'SSP/RO'),
    ('SSP/RR', 'SSP/RR'),
    ('SSP/SC', 'SSP/SC'),
    ('SSP/SP', 'SSP/SP'),
    ('SSP/SE', 'SSP/SE'),
    ('SSP/TO', 'SSP/TO'),
    ('UF', 'UF'),
    ('Undefined ', 'Undefined'),
]
ESTADO_CIVIL_CHOICES = [
    ('solteiro', 'solteiro'),
    ('solteira', 'solteira'),
    ('casado', 'casado'),
    ('casada', 'casada'),
    ('divorciado', 'divorciado'),
    ('divorciada', 'divorciada'),
    ('viúvo', 'viúvo'),
    ('viúva', 'viúva'),
    ('união estável', 'união estável'),  # Mantido original para consistência
    ('separado judicialmente', 'separado judicialmente'),
    ('separada judicialmente', 'separada judicialmente'),
    ('Undefined ', 'Undefined'),

]
SEXO_CHOICES = [
    ('Masculino', 'Masculino'),
    ('Feminino', 'Feminino'),
    ('Undefined ', 'Undefined'),
]

ETNIA_CHOICES = [
    ('Branco', 'Branco'),
    ('Pardo', 'Pardo'),
    ('Preto', 'Preto'),
    ('Amarelo', 'Amarelo'),
    ('Indígena', 'Indígena'),
    ('Outro', 'Outro'),
    ('Undefined ', 'Undefined'),
]
ESCOLARIDADE_CHOICES = [
    ('Analfabeto', 'Analfabeto'),
    ('Primário 1/4 série', 'Primário 1/4 série'),
    ('Fundamental', 'Fundamental'),
    ('Ensino Médio', 'Ensino Médio'),
    ('Ensino Superior', 'Ensino Superior'),
    ('Undefined ', 'Undefined'),
]

RECOLHE_INSS_CHOICES = [
    ('Sim', 'Sim'),
    ('Não', 'Não'),
    ('Undefined ', 'Undefined'),
]
MESES = [
    ('04', 'Abril'),
    ('05', 'Maio'),
    ('06', 'Junho'),
    ('07', 'Julho'),
    ('08', 'Agosto'),
    ('09', 'Setembro'),
    ('10', 'Outubro'),
    ('11', 'Novembro'),

]
STATUS_EMISSAO_INSS = [
    ('pendente', 'Pendente'),
    ('emitido', 'Emitido'),
    ('pago', 'Pago'),
    ('atrasada', 'Atrasada'),
]
STATUS_RESPOSTAS_REAP = [
    ('pendente', 'Pendente'),
    ('emitido', 'Emitido'),
    ('pago', 'Pago'),
    ('atrasada', 'Atrasada'),
]
ACESSO_CHOICES = [
    ('validar_codigo_acesso', 'Validar Código Acesso'),
    ('senha_invalida', 'Senha Inválida'),
    ('nivel_conta_insuficiente', 'Nível Conta Insuficiente'),
    ('sem_caepf', 'Sem CAEPF'),
    ('sem_login', 'Sem Login'),
    ('ok', 'OK'),
]
STATUS_PROCESSAMENTO = (
    ('usuario_processando', 'Usuário Processando'),
    ('Processada', 'Processada'),
    ('aguardando_processamento', 'Aguardando Processamento'),
)


SEGURO_DEFESO_CHOICES = [
    ('Não Recebe', 'Não Recebe'),
    ('Recebe', 'Recebe'),
    ('Undefined ', 'Undefined'),
]
JA_RECEBEU_DEFESO_ALGUMA_VEZ = [
    ('Sim', 'Sim'),
    ('Não', 'Não'),
    ('Undefined ', 'Undefined'),  
]
RELACAO_TRABALHO_CHOICES = [
    ('Indicidual Autônomo', 'Individual Autônomo'),
    ('Economia Familiar', 'Economia Familiar'),
    ('Regime de Parceria', 'Regime de Parceria'),
    ('Undefined ', 'Undefined'),
]
COMERCIALIZACAO_CHOICES = [
    ('Sim', 'Sim'),
    ('Não', 'Não'),
    ('Undefined ', 'Undefined'),
]
OUTRA_FONTE_RENDA = [
    ('Não Possui', 'Não Possui'),
    ('Aposentadoria (INSS)', 'Aposentadoria (INSS)'),
    ('MEI', 'MEI'),
    ('Sócio de Empresa', 'Sócio de Empresa'),
    ('CLT', 'CLT'),
    ('Servidor Público', 'Servidor Público'),
    ('Undefined ', 'Undefined'),
]

BOLSA_FAMILIA_CHOICES = [
    ('Já recebeu', 'Já recebeu'),
    ('Nunca recebeu', 'Nunca recebeu'),
    ('Undefined ', 'Undefined'),
]
CASA_ONDE_MORA = [
    ('Mora em casa prórpia', 'Mora em pasa prórpia'),
    ('Mora em casa augada', 'Mora em casa augada'),
    ('Mora em casa cedida', 'Mora em casa cedida'),
    ('Mora em casa de terceiros', 'Mora em casa de terceiros'),
    ('Undefined ', 'Undefined'),
]

STATUS_CHOICES = [
    ('associado_lista_ativo', 'Associado Lista Ativos(a)'),
    ('associado_lista_aposentado', 'Associado Lista Aposentados(a)'),
    ('candidato', 'Candidato(a)'),
    ('cliente_especial', 'Cliente Especial'),
    ('extra_associado', 'Extra Associado(a)'),
    ('desassociado', 'Desassociado(a)'),
]

ESPECIES_MARITIMAS = [
    ('Abrótea', 'Abrótea (Phycis phycis)'),
    ('Anchova', 'Anchova (Pomatomus saltatrix)'),
    ('Atum', 'Atum (Thunnus spp.)'),
    ('Bagre', 'Bagre (Siluriformes)'),
    ('Baiacu', 'Baiacu (Tetraodontidae)'),
    ('Camarão Branco', 'Camarão Branco (Litopenaeus schmitti)'),
    ('Camarão Rosa', 'Camarão Rosa (Farfantepenaeus paulensis)'),    
    ('Cação', 'Cação (Ginglymostomatidae)'),
    ('Cavala', 'Cavala (Scomberomorus cavalla)'),
    ('Corvina', 'Corvina (Micropogonias furnieri)'),
    ('Garoupa', 'Garoupa (Epinephelus marginatus)'),
    ('Linguado', 'Linguado (Paralichthys orbignyanus)'),
    ('Marisco', 'Marisco (Bivalvia)'),
    ('Pampo', 'Pampo (Trachinotus carolinus)'),
    ('Parati', 'Parati (Mugil curema)'),         
    ('Pescada Olhuda', 'Pescada Olhuda (Cynoscion guatucupa)'),
    ('Pescada Branca', 'Pescada Branca (Cynoscion leiarchus)'),    
    ('Robalo', 'Robalo (Centropomus undecimalis)'),
    ('Sardinha', 'Sardinha (Sardinella brasiliensis)'),
    ('Tainha', 'Tainha (Mugil liza)'),
    ('Xerelete', 'Xerelete (Caranx hippos)'),
    ('Não declarado', 'Não declarado'),
]

TIPO_MODELOS_MAP = {
    'associado': ('app_associados', 'associadomodel'),
    'associacao': ('app_associacao', 'associacaomodel'),
    'reparticao': ('app_associacao', 'reparticoesmodel'),
}

# Choices para o tipo de ato normativo (para o campo 'tipo' em Portaria, por exemplo)
TIPO_ATO_NORMATIVO_CHOICES = [
    ('FEDERAL', 'Federal'),
    ('ESTADUAL', 'Estadual'),
    ('MUNICIPAL', 'Municipal'),
]

# Choices para o status do benefício
STATUS_BENEFICIO_CHOICES = [
    ('EM_PREPARO', 'Em Preparo'),
    ('PROTOCOLADO_EM_ANALISE', 'Protocolado, em Análise'),
    ('CUMPRIDA_EXIGENCIA_EM_ANALISE', 'Exigência cumprida, em Análise'),
    ('CONCEDIDO', 'Concedido'),
    ('NEGADO', 'Negado'),
    ('RECURSO', 'Recurso'),
    ('CANCELADO', 'Cancelado'),
]
