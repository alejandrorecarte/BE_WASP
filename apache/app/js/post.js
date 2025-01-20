let vehicles = [];

window.onload = function () {
    verificarSesion();
    const params = new URLSearchParams(window.location.search);
    let post_id = parseInt(params.get('post_id'));
    loadPost(post_id);
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
        window.location.href = '../index.html';
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
                } else {
                    // Si la respuesta no es OK (por ejemplo, token inválido o expirado), mostrar los botones de login
                    console.log("Cookie not verified")
                    window.location.href = '../index.html';
                }
            })
            .catch(error => {
                console.error('Error al verificar la sesión:', error);
            });
    }
}

function loadPost(post_id) {
    fetch(`/api/post/get?post_id=${post_id}`, {
        method: 'GET'
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.post) {
                const post = data.post;
                document.getElementById('postTitle').value = post.title;
                document.getElementById('postDescription').innerText = post.description;

                fetch(`/api/vehicle/post?post_id=${post_id}`, {
                    method: 'GET'
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        if (data.vehicles) {
                            vehicles = data.vehicles;
                            for (let vehicle of vehicles){
                                addVehicleToList(vehicle);
                            }

                        } else {
                            console.error('Error: data.post is not an object');
                        }
                })
            } else {
                console.error('Error: data.post is not an object');
            }
    })
}

function addVehicleToList(vehicleItem) {
    const vehicleList = document.getElementById('vehicleList');
    const vehicleDiv = document.createElement('div');
    vehicleDiv.classList.add('vehicle-item');

    if (!vehicleItem.photo) {
        console.log("No photo available for this vehicle"); // Si no hay foto, muestra un mensaje
        return;
    }

    // Asegurarse de que vehicleItem.photo esté correctamente formateado para base64
    const imageBase64 = `data:image/png;base64,${vehicleItem.photo}`;
    
    // Creamos el contenido HTML para el vehículo
    vehicleDiv.innerHTML = `
        <h3>${vehicleItem.brand} ${vehicleItem.model} (${vehicleItem.registration_year})</h3>
        <p>Precio: $${vehicleItem.price}</p>
        <p>${vehicleItem.observations}</p>
        <p>Tipo de Vehículo: ${vehicleItem.vehicleType}</p>
        <p>Combustible: ${vehicleItem.fuelType}</p>
        <p>Matrícula: ${vehicleItem.license_plate}</p>
        <img src="${imageBase64}" alt="Foto del vehículo" style="width: 100px; margin: 5px;">
    `;

    vehicleList.appendChild(vehicleDiv);
}

