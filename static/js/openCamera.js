// openCamera.js
function abrirCamera() {
    const input = document.querySelector('#uploadCameraForm input[type="file"]');
    if (input) {
        input.click();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    if (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
        document.querySelectorAll('.camera-upload-mobile').forEach(el => {
            el.style.display = 'inline-block';
        });
    }
});