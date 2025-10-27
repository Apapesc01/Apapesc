
//Mascaras

// CPF
var cpfInput = document.querySelector('#id_cpf');
if (cpfInput) {
    IMask(cpfInput, { mask: '000.000.000-00' });
}

// Celular
var celInput = document.querySelector('#id_celular');
if (celInput) {
    IMask(celInput, {
        mask: [
            { mask: '(00)00000-0000' },
            { mask: '(00)0000-0000' }
        ]
    });
}
var celInput = document.querySelector('#id_celular_correspondencia');
if (celInput) {
    IMask(celInput, {
        mask: [
            { mask: '(00)00000-0000' },
            { mask: '(00)0000-0000' }
        ]
    });
}
// Máscara CEP
var cepInput = document.querySelector('#id_cep');
if (cepInput) {
    IMask(cepInput, {
        mask: '00000-000'
    });
}

// Máscara CNPJ
var cnpjInput = document.querySelector('#id_cnpj');
if (cnpjInput) {
    IMask(cnpjInput, {
        mask: '00.000.000/0000-00'
    });
}