
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
    ('respondido', 'Respondido'),
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
    ('Mora em casa prórpia', 'Mora em casa prórpia'),
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


NATUREZA_SERVICO_CHOICES = [
    ('assessoria', 'Assessoria'),    
    ('consultoria', 'Consultoria'),           
    ('emissao_documento', 'Emissão e Documento'),

]

TIPO_SERVICO = [
    # Assessoria
    ('assessoria_administrativa', 'Assessoria Administrativa (Recursos)'),    
    ('assessoria_processo_paa', 'Assessoria Processo PAA'),     
    ('assessoria_processo_pronaf', 'Assessoria Processo PRONAF'),
    
    # Emissão
    ('emissao_tie', 'Emissão de TIE'),
    ('emissao_rgp', 'Emissão de RGP'),
    ('emissao_licanca_pesca', 'Emissão Licença Pesca'),
    ('emissao_pop', 'Emissão Carteira POP'),   

    # Consultorias
    ('consultoria_geral', 'Consultoria Geral'),
]



STATUS_EMISSAO_DOC = [
    ('pendente', 'Pendente'),
    ('protocolado_analise', 'Protocolado, em Análise'),
    ('exigencia_cumprida', 'Exigencia cumprida, em análise'),
    ('deferido', 'Documento Deferido'),
    ('indeferido', 'Documento Indeferido'),
    ('recurso', 'Recurso'),
    ('pedido_cancelado', 'Pedido Cancelado'),
]

STATUS_ASSESSORIA_PROCESSO = [
    ('agendada', 'Agendada'),
    ('processo_preparo', 'Processo em Preparo'),
    ('processo_protocolado_analise', 'Protocolado, em Análise'),
    ('processo_exigencia_cumprida', 'Exigencia cumprida, em análise'),
    ('processo_deferido', 'Documento Deferido'),
    ('processo_indeferido', 'Documento Indeferido'),
    ('processo_recurso_preparo', 'Recurso em Preparo'),
    ('processo_recurso_protocolado', 'Recurso Protocolado'),
    ('processo_recurso_concedido', 'Recurso Concedido'),
    ('processo_recurso_negado', 'Recurso Negado'),
    ('processo_pedido_cancelado', 'Pedido Cancelado'),
]   

STATUS_CONSULTORIA = [
    ('agendada', 'Agendada'),
    ('concluida', 'Concluída'),
    ('cancelada', 'Cancelada'),
]

FORMA_PAGAMENTO_CHOICES = [
    ('pix', 'PIX'),
    ('credito', 'Cartão de Crédito'),
    ('debito', 'Cartão de Débito'),
    ('deposito', 'Depósito'),
    ('dinheiro', 'Dinheiro'),
]

PARCELAMENTO_CHOICES = [
    ('avista', 'Pagamento à Vista'),
    ('duas_parcelas', 'Duas Parcelas'),
    ('tres_parcelas', 'Três Parcelas'),
]

STATUS_PAGAMENTO_CHOICES = [
    ('pendente', 'Pendente'),
    ('parcial', 'Parcial'),
    ('pago', 'Pago'),
]
STATUS_COBRANCA = ["extra_associado", "cliente_especial", "desassociado"]

# Embarcações
TIPO_EMBARCACAO = [
    ('canoa', 'Canoa'),  
    ('bote', 'Bote'),  
    ('traineira', 'Traineira'),  
    ('atuaneiro', 'Atuaneiro'), 
    ('Outro', 'Outro'),     
                      
]
PROPULSAO = [
    ('motor', 'Motor'),
    ('vela', 'Vela'),    
    ('remo', 'Remo'),
    ('outro', 'Outro'),    

]
COMBUSTIVEL_CHOICES = [
    ('alcool', 'Álcool'),        
    ('bateria', 'Bateria'),  
    ('diesel', 'Diesel'),              
    ('gasolina', 'Gasolina'),
    ('gas', 'Gás'),
    ('nao usa','Não Usa')
]

ALIENACAO_CHOICES = [
    ('sim', 'Sim'),
    ('nao', 'Não'),
]

PORTE_EMBARCACAO = [
    ('miuda', 'Miuda'),
    ('maior porte', 'Maior Porte')        
]

SEGURO_DPEM_CHOICES = [
    ('sim', 'Sim'),
    ('nao', 'Não'),
]

NOME_LICENCA_CHOICES = [
    ('registro_licenca_embarcacao', 'Certificado de Registro e Autorização de Embarcação Pesqueira'),
    # adicione mais
]
ORGAO_EMISSOR_LICENCA = [
    ('MAPA', 'Ministério da Agricultura, Pecuária e Abastecimento'),
    ('IBAMA', 'IBAMA'),
    ('MMA', 'Ministério do Meio Ambiente'),
    ('SPU', 'Secretaria do Patrimônio da União'),
    # adicione mais se necessário
]

# App Despesas
TIPO_DESPESA_CHOICES = [
    ('aluguel', 'Aluguel'),
    ('internet', 'Internet'),
    ('tranposrte', 'Transporte'),
    ('uber', 'Uber'),
    ('gcp_hospedagem', 'GCP/Hospedagem'),
    ('matuntencao', 'Manutenção'),
    ('pagamento_honorarios', 'Pagamento/Honorários'),
    ('credito_celular', 'Crédito Celular'),
    ('prestacao_servicos', 'Prestação de Serviços'),
    ('papelaria', 'Papelaria'),
    ('outros', 'Outros'),
    
]
