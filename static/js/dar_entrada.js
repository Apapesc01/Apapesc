
document.addEventListener("DOMContentLoaded", function () {
    const select = document.querySelector("select[name='dar_entrada']");

    if (!select) {
        console.log("ERRO: Campo dar_entrada não encontrado no DOM.");
        return;
    }

    console.log("Valor atual:", select.value);

    function aplicarCor() {
        select.classList.remove("select-dez", "select-jan", "select-fev", "select-mar");

        if (select.value === "DEZ") select.classList.add("select-dez");
        else if (select.value === "JAN") select.classList.add("select-jan");
        else if (select.value === "FEV") select.classList.add("select-fev");
        else if (select.value === "MAR") select.classList.add("select-mar");
    }

    aplicarCor();
    select.addEventListener("change", aplicarCor);
});


