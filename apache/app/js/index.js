// Llamar a la función al cargar la página
window.onload = function () {
    verificarSesion();
}

// Obtener el valor de una cookie por su nombre
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Verificar si el usuario está autenticado
function verificarSesion() {
    const token = getCookie('access_token'); // Obtener el token de la cookie

    if (token === null) {
        console.log("No cookies")
    }
    else {
        console.log("Verifying cookie")
        fetch('/api/secure-endpoint', {
            method: 'GET'
        })
            .then(response => {
                if (response.ok) {
                    // Si la respuesta es OK (status 200), el token es válido
                    console.log("Cookie verified")
                    window.location.href = '/img/home.html';
                } else {
                    // Si la respuesta no es OK (por ejemplo, token inválido o expirado), mostrar los botones de login
                    console.log("Cookie not verified")
                }
            })
            .catch(error => {
                console.error('Error al verificar la sesión:', error);
            });
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("registerButton").addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = '/img/register.html';  // Asegúrate de que la ruta sea la correcta
    });

    // Obtener el formulario y agregar el evento de submit
    document.getElementById('form').addEventListener('submit', function (event) {
        event.preventDefault();  // Prevenir el comportamiento por defecto del formulario

        // Recoger los datos del formulario
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Construimos la URL con los parámetros codificados
        const url = `/api/users/login`;

        // Enviar los datos al backend
        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/img/home.html';
                } else {
                    alert('Hubo un problema al iniciar sesión');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un problema al iniciar sesión');
            });
    });
});