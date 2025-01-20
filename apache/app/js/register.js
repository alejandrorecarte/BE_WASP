// Obtener el formulario y agregar el evento de submit
document.getElementById('form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevenir el comportamiento por defecto del formulario

    // Recoger los datos del formulario
    const email = document.getElementById('email').value;
    const name = document.getElementById('name').value;
    const last_name = document.getElementById('surname').value;
    const password = document.getElementById('password').value;

    // Construimos la URL con los parámetros codificados
    const url = `/api/users/register`;

    // Enviar los datos al backend
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: email,
            name: name,
            last_name: last_name,
            password: password
        })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/';  // Redirigir a la página principal
        }else{
            alert('Hubo un problema al registrarse');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema al registrarse');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("backButton").addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = "../index.html";
    })
});