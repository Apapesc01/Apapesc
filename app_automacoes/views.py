from core.views.base_imports import*
from core.views.app_automacoes_imports import *


# Mapeamento de automações para modelos
MODELO_MAP = {
    'residencia': DeclaracaoResidenciaModel,
    #'filiacao': DeclaracaoFiliacaoModel,
    #'atividade_pesqueira': DeclaracaoAtividadePesqueiraModel,
    #'hipossuficiencia': DeclaracaoHipossuficienciaModel,
    #'procuracao_juridica': ProcuracaoJuridicaModel,
    #'recibos_anuidades': ReciboAnuidadeModel,
    #'recibos_servicos_extra': ReciboServicoExtraModel,
    #'carteirinha_apapesc': CarteirinhaAssociadoModel,
    #'cobranca_anuidades': CobrancaAnuidadeModel,
    #'procuracao_administrativa': ProcuracaoAdministrativaModel,
    #'autorizacao_direito_imagem': AutorizacaoDireitoImagemModel,
    #'autorizacao_acesso_gov': AutorizacaoAcessoGovModel,
    #'declaracao_desfiliacao': DeclaracaoDesfiliacaoModel,
    #'direitos_deveres':DireitosDeveres,
    #'retirada_documentos': RetiradaDocumentos,

}

# UPLOAD DE MODELOS PDF BASE
def upload_pdf_base(request, automacao):
    modelo_map = {
        'residencia': DeclaracaoResidenciaModel,
        #'filiacao': DeclaracaoFiliacaoModel,
        #'atividade_pesqueira': DeclaracaoAtividadePesqueiraModel,
        #'hipossuficiencia': DeclaracaoHipossuficienciaModel,
        #'procuracao_juridica': ProcuracaoJuridicaModel,
        #'recibos_anuidades': ReciboAnuidadeModel,
        #'recibos_servicos_extra': ReciboServicoExtraModel,
        #'carteirinha_apapesc': CarteirinhaAssociadoModel,
        #'cobranca_anuidades': CobrancaAnuidadeModel,
        #'procuracao_administrativa': ProcuracaoAdministrativaModel,
        #'autorizacao_direito_imagem': AutorizacaoDireitoImagemModel,
        #'autorizacao_acesso_gov': AutorizacaoAcessoGovModel,
        #'declaracao_desfiliacao': DeclaracaoDesfiliacaoModel,
        #'direitos_deveres':DireitosDeveres,
        #'retirada_documentos': RetiradaDocumentos,
    }
    
    modelo = modelo_map.get(automacao)
    if not modelo:
        return HttpResponse("Automação inválida.", status=400)

    if request.method == "POST":
        pdf_base = request.FILES.get('pdf_base')
        if not pdf_base:
            return HttpResponse("Arquivo PDF não enviado.", status=400)

        # Tenta pegar a primeira instância existente; se não houver, cria nova
        instancia = modelo.objects.first()
        if not instancia:
            instancia = modelo()

        # Atribui o novo arquivo e salva
        instancia.pdf_base = pdf_base
        instancia.save()

        return redirect('app_automacoes:lista_automacoes')  # Ajuste conforme sua url de destino

    # Para requisições GET, exibe o template com formulário de upload
    return render(request, 'automacoes/upload_pdf_base.html', {'automacao': automacao})


class ListaTodosArquivosView(LoginRequiredMixin, TemplateView):
    template_name = 'automacoes/list_automacoes.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicione cada queryset com nome separado
        context['declaracoes_residencia'] = DeclaracaoResidenciaModel.objects.all()
        #context['declaracoes_filiacao'] = DeclaracaoFiliacaoModel.objects.all()
        #context['declaracoes_atividade_pesqueira'] = DeclaracaoAtividadePesqueiraModel.objects.all()
        #context['declaracoes_hipossuficiencia'] = DeclaracaoHipossuficienciaModel.objects.all()
        #context['procuracoes_procuracao_juridica'] = ProcuracaoJuridicaModel.objects.all()
        #context['recibos_anuidades'] = ReciboAnuidadeModel.objects.all()
        #context['recibos_servicos_extra'] = ReciboServicoExtraModel.objects.all()
        #context['carteirinha_apapesc'] = CarteirinhaAssociadoModel.objects.all()
        #context['cobranca_anuidades'] = CobrancaAnuidadeModel.objects.all()
        #context['procuracoes_procuracao_administrativa'] = ProcuracaoAdministrativaModel.objects.all()
        #context['autorizacao_direito_imagem'] = AutorizacaoDireitoImagemModel.objects.all()
        #context['autorizacao_acesso_gov'] = AutorizacaoAcessoGovModel.objects.all()
        #context['declaracao_desfiliacao'] = DeclaracaoDesfiliacaoModel.objects.all()
        #context['direitos_deveres'] = DireitosDeveres.objects.all()
        #context['retirada_documentos'] = RetiradaDocumentos.objects.all()
        
        return context


# Automações

# PÁGINA DE AÇÕES -  AS AÇÕES GERAR ESTÃO VÍNCULADAS NESSA PÁGINA
def pagina_acoes(request, associado_id=None):
    pdf_url = request.GET.get('pdf_url')

    associado = None

    if associado_id:
        associado = get_object_or_404(AssociadoModel, pk=associado_id)
    

    return render(request, 'automacoes/pagina_acoes.html', {
        'pdf_url': pdf_url,
        #'tipo_recibo': tipo_recibo,
        #'associado': associado,
        #'entrada': entrada,
        #'extra_associado': extra_associado,
        #'associacao': associacao,
    })



#=======================================================================================================


# GERAR DECLARAÇÃO DE RESIDÊNCIA
def gerar_declaracao_residencia(request, associado_id):
    associado = AssociadoModel.objects.get(id=associado_id)
    associacao = associado.associacao
        
    # Caminho para o PDF de template
    template_path = os.path.join(settings.MEDIA_ROOT, 'pdf/declaracao_residencia.pdf')
    if not os.path.exists(template_path):
        return HttpResponse("O PDF base para a Declaração de Residência não foi encontrado.", status=404)

    template_pdf = PdfReader(template_path)
    template_page = template_pdf.pages[0]  # Primeira página como template

    # Buffer em memória para o conteúdo dinâmico
    buffer = BytesIO()

    # Definindo estilos personalizados
    styles = getSampleStyleSheet()
    style_title = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Times-Bold',
        fontSize=16,
        alignment=1,  # Centralizado
        leading=32,  # Espaçamento entre as linhas do título
        spaceBefore=100,  # Espaçamento antes do título
        textColor=colors.grey,
    )
    style_normal = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=28,  # Espaçamento entre linhas
        alignment=4,  # Justificado
    )
    style_assinatura = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=28,  # Espaçamento entre linhas
        alignment=1,  # Centralizado
    )
    style_data = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=28,  # Espaçamento entre linhas
        alignment=0,  # Esquerda
        spaceBefore=20,  # Espaçamento antes do título
    )
    # Data atual
    data_atual = datetime.now().strftime('%d/%m/%Y')

    # Texto da declaração
    texto = (
        f"Eu, <strong>{associado.user.get_full_name()}</strong>, inscrito no CPF nº {associado.cpf}, na falta de documentos "
        f"para comprovação de residência, em conformidade com o disposto na Lei 7.115, de 29 de "
        f"agosto de 1983, DECLARO para os devidos fins, sob penas da Lei, que RESIDO no endereço: "
        f"<strong>{associado.logradouro}, nº {associado.numero}, {associado.complemento},"
        f" {associado.bairro}, {associado.municipio} - {associado.uf}, CEP: {associado.cep}.</strong>"
    )

    # Declaração de veracidade
    declaracao_veracidade = (
        "Declaro sob as penas da lei (Art. 299 do Código Penal) a veracidade das informações "
        "aqui prestadas para emissão desta declaração, ficando sob minha responsabilidade as "
        "informações nelas contidas e eventuais informações não declaradas."
    )

    # Local e data
    local_data = f"FLORIANÓPOLIS, {data_atual}."

    # Assinatura
    assinatura = (
        "____________________________________________________________________<br/>"
        f"{associado.user.get_full_name()}  - CPF: {associado.cpf}<br/>"
    )

    # Elementos do PDF na ordem correta
    elements = [
        Paragraph("DECLARAÇÃO DE RESIDÊNCIA", style_title),
        Spacer(1, 20),
        Paragraph(texto, style_normal),
        Spacer(1, 10),
        Paragraph(declaracao_veracidade, style_normal),
        Paragraph(local_data, style_data),
        Spacer(1, 24),
        Paragraph(assinatura, style_assinatura),
        Spacer(1, 26),
    ]

    # Criação do documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=85,
        leftMargin=85,
        topMargin=160,
        bottomMargin=40,
    )

    # Gerar o conteúdo do PDF
    doc.build(elements)

    # Mesclar o conteúdo dinâmico com o template PDF
    buffer.seek(0)
    overlay_pdf = PdfReader(buffer)
    overlay_page = overlay_pdf.pages[0]

    merger = PageMerge(template_page)
    merger.add(overlay_page).render()

    # Salvar o PDF em disco
    pdf_name = f"declaracao_residencia_{associado.user.get_full_name().replace(' ', '_')}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'documentos', pdf_name)
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    PdfWriter(pdf_path, trailer=template_pdf).write()

    # Construir o URL para o PDF
    pdf_url = f"{settings.MEDIA_URL}documentos/{pdf_name}"

    # Redirecionar para a página de ações
    query_string = urlencode({'pdf_url': pdf_url})
    redirect_url = f"{reverse('app_automacoes:pagina_acoes', kwargs={'associado_id': associado.id})}?{query_string}"
    return redirect(redirect_url)
# =======================================================================================================