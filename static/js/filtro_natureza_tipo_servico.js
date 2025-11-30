
const tiposPorNatureza = {
    "assessoria": [
        {value: "assessoria_administrativa", label: "Assessoria Administrativa (Recursos)"},
        {value: "assessoria_administrativa_correcao_dados", label: "Assessoria Administrativa (Correção de dados)"},
        {value: "assessoria_processo_paa", label: "Assessoria Processo PAA"},
        {value: "assessoria_processo_pronaf", label: "Assessoria Processo PRONAF"},
    ],
    "emissao_documento": [
        {value: "emissao_tie", label: "Emissão de TIE"},
        {value: "emissao_rgp", label: "Emissão de RGP"},
        {value: "emissao_licanca_pesca", label: "Emissão Licença Pesca"},
        {value: "emissao_pop", label: "Emissão Carteira POP"},
    ],
    "consultoria": [
        {value: "consultoria_geral", label: "Consultoria Geral"},
    ]
};

function atualizarTipoServico() {
    const natureza = document.querySelector(".js-natureza-servico");
    const tipo = document.querySelector(".js-tipo-servico");
    const naturezaSelecionada = natureza.value;

    // Salva valor selecionado antes de resetar
    const valorAnterior = tipo.value;

    // Limpa opções
    tipo.innerHTML = '<option value="">---------</option>';

    if (tiposPorNatureza[naturezaSelecionada]) {
        tiposPorNatureza[naturezaSelecionada].forEach(opt => {
            const option = document.createElement('option');
            option.value = opt.value;
            option.text = opt.label;
            // Seleciona valor anterior, se houver
            if (opt.value === valorAnterior) option.selected = true;
            tipo.appendChild(option);
        });
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const natureza = document.querySelector(".js-natureza-servico");
    if (natureza) {
        atualizarTipoServico(); // já filtra ao carregar, útil para edição
        natureza.addEventListener("change", atualizarTipoServico);
    }
});

