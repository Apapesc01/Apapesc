// logica_desfiliacao_refiliacao.js
document.addEventListener('DOMContentLoaded', function () {
    const statusField = document.getElementById('id_status');
    const dataDesfiliacaoField = document.getElementById('campo-data-desfiliacao');

    function toggleDesfiliacao() {
        if (statusField.value === 'desassociado') {
            dataDesfiliacaoField.style.display = 'block';
        } else {
            dataDesfiliacaoField.style.display = 'none';
        }
    }

    statusField.addEventListener('change', toggleDesfiliacao);
    toggleDesfiliacao();  // executa ao carregar
});