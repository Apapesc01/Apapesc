document.addEventListener("DOMContentLoaded", () => {
    fetch("/graficos/dados/defeso/")
        .then(res => res.json())
        .then(data => {
            console.log("DADOS RECEBIDOS:", data);

            buildChartEspecies(data);
            buildChartEstados(data);
            buildChartAnos(data);
            buildChartStatusBeneficio(data);
            buildChartConcedidoNegado(data);
            buildChartStatusProcessamento(data);
            buildChartEntradaMes(data);
        })
        .catch(err => console.error("Erro ao carregar dados dos gráficos:", err));
});

/* ---------------- GRÁFICO 1 - ESPÉCIES ---------------- */
function buildChartEspecies(data) {
    const ctx = document.getElementById("chartEspecies");
    if (!ctx) return;

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.especies,
            datasets: [{
                label: "Benefícios",
                data: data.especies_totais,
                backgroundColor: "#60a5fa"
            }]
        }
    });
}

/* ---------------- GRÁFICO 2 - ESTADOS ---------------- */
function buildChartEstados(data) {
    const ctx = document.getElementById("chartEstados");
    if (!ctx) return;

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.estados,
            datasets: [{
                label: "Total",
                data: data.estados_totais,
                backgroundColor: "#34d399"
            }]
        },
        options: {
            indexAxis: "y"
        }
    });
}

/* ---------------- GRÁFICO 3 - ANOS ---------------- */
function buildChartAnos(data) {
    const ctx = document.getElementById("chartAnos");
    if (!ctx) return;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: data.anos,
            datasets: [{
                label: "Benefícios",
                data: data.anos_totais,
                borderColor: "#f59e0b",
                tension: 0.3
            }]
        }
    });
}

/* ---------------- GRÁFICO 4 - STATUS DO BENEFÍCIO ---------------- */
function buildChartStatusBeneficio(data) {
    const ctx = document.getElementById("chartStatusBeneficio");
    if (!ctx) return;

    // Mapa de cores definido por significado
    const colorMap = {
        "Em Preparo": "#3b82f6",                      // azul
        "Protocolado, em Análise": "#22c55e",         // verde médio
        "Em Exigência": "#eab308",                    // amarelo
        "Exigência cumprida, em Análise": "#fb923c",  // laranja
        "Concedido": "#15803d",                       // verde escuro
        "Negado": "#dc2626",                          // vermelho forte
        "Recurso": "#7c3aed",                         // roxo
        "Cancelado": "#6b7280"                        // cinza escuro
    };

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: data.dados_status_beneficio.map(x => x.label),
            datasets: [{
                data: data.dados_status_beneficio.map(x => x.value),
                backgroundColor: data.dados_status_beneficio.map(x =>
                    colorMap[x.label] || "#a3a3a3" // fallback cinza
                )
            }]
        }
    });
}


/* ---------------- GRÁFICO 5 - CONCEDIDOS vs NEGADOS ---------------- */
function buildChartConcedidoNegado(data) {
    const ctx = document.getElementById("chartConcedidoNegado");
    if (!ctx) return;

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.dados_concedido_negado.labels,
            datasets: [{
                data: data.dados_concedido_negado.values,
                backgroundColor: ["#10b981", "#ef4444"]
            }]
        },
        options: {
            plugins: { legend: { display: false } }
        }
    });
}

/* ---------------- GRÁFICO 6 - STATUS DE PROCESSAMENTO ---------------- */
function buildChartStatusProcessamento(data) {
    const ctx = document.getElementById("chartStatusProcessamento");
    if (!ctx) return;

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: data.dados_status_processamento.map(x => x.label),
            datasets: [{
                data: data.dados_status_processamento.map(x => x.value),
                backgroundColor: ["#60a5fa","#22c55e","#facc15"]
            }]
        }
    });
}

/* ---------------- GRÁFICO 7 - ENTRADA POR MÊS (DAR_ENTRADA) ---------------- */
function buildChartEntradaMes(data) {
    const ctx = document.getElementById("chartEntradaMes");
    if (!ctx) return;

    // Cores específicas para cada mês
    const colorMap = {
        "Dezembro": "#86efac",   // verde claro
        "Janeiro": "#fde047",    // amarelo
        "Fevereiro": "#d946ef",  // rosa/purple
        "Março": "#fda4a4"       // vermelho claro
    };    

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.dados_entrada_mes.map(x => x.label),
            datasets: [{
                label: "Entradas",
                data: data.dados_entrada_mes.map(x => x.value),
                backgroundColor: data.dados_entrada_mes.map(x => colorMap[x.label] || "#60a5fa")
            }]
        },
        options: {
            plugins: { legend: { display: false } }
        }
    });
}

