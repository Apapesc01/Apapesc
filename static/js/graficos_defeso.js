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

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: data.dados_status_beneficio.map(x => x.label),
            datasets: [{
                data: data.dados_status_beneficio.map(x => x.value),
                backgroundColor: ["#60a5fa","#34d399","#fbbf24","#f87171","#a78bfa","#f472b6","#2dd4bf","#c084fc"]
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
