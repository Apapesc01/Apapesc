
const statusPorTipoServico = {
    "assessoria_administrativa": [
        {value: "agendada", label: "Agendada"},
        {value: "processo_preparo", label: "Processo em Preparo"},
        {value: "processo_protocolado_analise", label: "Protocolado, em Análise"},
        {value: "processo_em_exigência", label: "Processo em Exigência"},
        {value: "processo_exigencia_cumprida", label: "Exigencia cumprida, em análise"},
        {value: "processo_deferido", label: "Documento Deferido"},
        {value: "processo_indeferido", label: "Documento Indeferido"},
        {value: "processo_recurso_preparo", label: "Recurso em Preparo"},
        {value: "processo_recurso_protocolado", label: "Recurso Protocolado"},
        {value: "processo_recurso_concedido", label: "Recurso Concedido"},
        {value: "processo_recurso_negado", label: "Recurso Negado"},
        {value: "processo_pedido_cancelado", label: "Pedido Cancelado"},
    ],
    "assessoria_administrativa_correcao_dados": [
        {value: "agendada", label: "Agendada"},
        {value: "processo_preparo", label: "Processo em Preparo"},
        {value: "processo_protocolado_analise", label: "Protocolado, em Análise"},
        {value: "processo_em_exigência", label: "Processo em Exigência"}, // NOVO ✔️
        {value: "processo_exigencia_cumprida", label: "Exigência cumprida, em análise"},
        {value: "processo_deferido", label: "Documento Deferido"},
        {value: "processo_indeferido", label: "Documento Indeferido"},
        {value: "processo_recurso_preparo", label: "Recurso em Preparo"},
        {value: "processo_recurso_protocolado", label: "Recurso Protocolado"},
        {value: "processo_recurso_concedido", label: "Recurso Concedido"},
        {value: "processo_recurso_negado", label: "Recurso Negado"},
        {value: "processo_pedido_cancelado", label: "Pedido Cancelado"},
    ],    
    "assessoria_processo_paa": [
        {value: "agendada", label: "Agendada"},
        {value: "processo_preparo", label: "Processo em Preparo"},
        {value: "processo_protocolado_analise", label: "Protocolado, em Análise"},
        {value: "processo_em_exigência", label: "Processo em Exigência"},
        {value: "processo_exigencia_cumprida", label: "Exigencia cumprida, em análise"},
        {value: "processo_deferido", label: "Documento Deferido"},
        {value: "processo_indeferido", label: "Documento Indeferido"},
        {value: "processo_recurso_preparo", label: "Recurso em Preparo"},
        {value: "processo_recurso_protocolado", label: "Recurso Protocolado"},
        {value: "processo_recurso_concedido", label: "Recurso Concedido"},
        {value: "processo_recurso_negado", label: "Recurso Negado"},
        {value: "processo_pedido_cancelado", label: "Pedido Cancelado"},
    ],
    "assessoria_processo_pronaf": [
        {value: "agendada", label: "Agendada"},
        {value: "processo_preparo", label: "Processo em Preparo"},
        {value: "processo_protocolado_analise", label: "Protocolado, em Análise"},
        {value: "processo_em_exigência", label: "Processo em Exigência"},
        {value: "processo_exigencia_cumprida", label: "Exigencia cumprida, em análise"},
        {value: "processo_deferido", label: "Documento Deferido"},
        {value: "processo_indeferido", label: "Documento Indeferido"},
        {value: "processo_recurso_preparo", label: "Recurso em Preparo"},
        {value: "processo_recurso_protocolado", label: "Recurso Protocolado"},
        {value: "processo_recurso_concedido", label: "Recurso Concedido"},
        {value: "processo_recurso_negado", label: "Recurso Negado"},
        {value: "processo_pedido_cancelado", label: "Pedido Cancelado"},
    ],
    "emissao_tie": [
        {value: "pendente", label: "Pendente"},
        {value: "protocolado_analise", label: "Protocolado, em Análise"},
        {value: "em_exigência", label: "Em Exigência"},
        {value: "exigencia_cumprida", label: "Exigencia cumprida, em análise"},
        {value: "deferido", label: "Documento Deferido"},
        {value: "indeferido", label: "Documento Indeferido"},
        {value: "recurso", label: "Recurso"},
        {value: "pedido_cancelado", label: "Pedido Cancelado"},
    ],
    "emissao_rgp": [
        {value: "pendente", label: "Pendente"},
        {value: "protocolado_analise", label: "Protocolado, em Análise"},
        {value: "em_exigência", label: "Em Exigência"},
        {value: "exigencia_cumprida", label: "Exigencia cumprida, em análise"},
        {value: "deferido", label: "Documento Deferido"},
        {value: "indeferido", label: "Documento Indeferido"},
        {value: "recurso", label: "Recurso"},
        {value: "pedido_cancelado", label: "Pedido Cancelado"},
    ],
    "emissao_licanca_pesca": [
        {value: "pendente", label: "Pendente"},
        {value: "protocolado_analise", label: "Protocolado, em Análise"},
        {value: "em_exigência", label: "Em Exigência"},
        {value: "exigencia_cumprida", label: "Exigencia cumprida, em análise"},
        {value: "deferido", label: "Documento Deferido"},
        {value: "indeferido", label: "Documento Indeferido"},
        {value: "recurso", label: "Recurso"},
        {value: "pedido_cancelado", label: "Pedido Cancelado"},
    ],
    "emissao_pop": [
        {value: "pendente", label: "Pendente"},
        {value: "protocolado_analise", label: "Protocolado, em Análise"},
        {value: "em_exigência", label: "Em Exigência"},
        {value: "exigencia_cumprida", label: "Exigencia cumprida, em análise"},
        {value: "deferido", label: "Documento Deferido"},
        {value: "indeferido", label: "Documento Indeferido"},
        {value: "recurso", label: "Recurso"},
        {value: "pedido_cancelado", label: "Pedido Cancelado"},
    ],    
    "consultoria_geral": [
        {value: "agendada", label: "Agendada"},
        {value: "concluida", label: "Concluída"},
        {value: "cancelada", label: "Cancelada"},
    ],
};

function atualizarStatusPorTipoServico() {
    const tipo = document.querySelector(".js-tipo-servico");
    const status = document.querySelector(".js-status-servico");
    const tipoSelecionado = tipo.value;

    const valorAnterior = status.value;
    status.innerHTML = '<option value="">---------</option>';

    if (statusPorTipoServico[tipoSelecionado]) {
        statusPorTipoServico[tipoSelecionado].forEach(opt => {
            const option = document.createElement('option');
            option.value = opt.value;
            option.text = opt.label;
            if (opt.value === valorAnterior) option.selected = true;
            status.appendChild(option);
        });
        // Se não tinha nada selecionado, seleciona o primeiro (após o "---------")
        if (!valorAnterior && status.options.length > 1) {
            status.options[1].selected = true;
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const tipo = document.querySelector(".js-tipo-servico");
    if (tipo) {
        atualizarStatusPorTipoServico(); // Inicializa ao abrir a página
        tipo.addEventListener("change", atualizarStatusPorTipoServico);
    }
});

