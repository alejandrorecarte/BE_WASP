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

// Inicializa el array de vehículos y el objeto de información de la flota
let vehicles = [];
let postInfo = {}; // Asegúrate de que postInfo contenga la información necesaria

// Obtener el formulario y agregar el evento de submit para la creación de la flota
document.getElementById('postForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto del formulario

    // Recoger los datos del formulario
    const title = document.getElementById('title').value.trim();
    const description = document.getElementById('description').value.trim();

    // Validar que los campos no estén vacíos
    if (!title || !description) {
        alert('Por favor, complete todos los campos.');
        return;
    }

    // Crear el objeto de parámetros
    postInfo = { title, description };
    document.getElementById('vehicleFormSection').style.display = 'block';
    document.getElementById('uploadVehiclesForm').style.display = 'block'; // Mostrar el formulario para subir vehículos
});

// Botón para añadir vehículo
document.getElementById('addVehicleBtn').addEventListener('click', function () {
    try {
        const license_plate = document.getElementById('license_plate').value;
        const brand = document.getElementById('brand').value;
        const model = document.getElementById('model').value;
        const registration_year = document.getElementById('registration_year').value;
        const price = document.getElementById('price').value;
        const observations = document.getElementById('observations').value;
        const vehicleType = document.getElementById('vehicleType').value;
        const fuelType = document.getElementById('fuelType').value;
        const photo = document.getElementById('photo').files[0]; // Asegúrate de obtener el archivo como tal

        // Validar campos requeridos
        if (!license_plate || !brand || !model || !registration_year || !price || !observations || !vehicleType || !fuelType || !photo) {
            throw new Error("Por favor, complete todos los campos requeridos.");
        }

        // Crear el objeto del vehículo
        const vehicleItem = {
            license_plate,
            brand,
            model,
            registration_year,
            price,
            observations,
            vehicleType,
            fuelType,
            photo // Guardamos el archivo directamente aquí, no base64
        };

        // Añadir el vehículo a la lista visual
        addVehicleToList(vehicleItem);

    } catch (error) {
        alert(error.message);
    }
});

// Función para añadir el vehículo a la lista visual
function addVehicleToList(vehicleItem) {
    const vehicleList = document.getElementById('vehicleList');
    const vehicleDiv = document.createElement('div');
    vehicleDiv.classList.add('vehicle-item');

    // Creamos el contenido HTML para el vehículo
    vehicleDiv.innerHTML = `
        <h3>${vehicleItem.brand} ${vehicleItem.model} (${vehicleItem.registration_year})</h3>
        <p>Precio: $${vehicleItem.price}</p>
        <p>${vehicleItem.observations}</p>
        <p>Tipo de Vehículo: ${vehicleItem.vehicleType}</p>
        <p>Combustible: ${vehicleItem.fuelType}</p>
        <p>Matrícula: ${vehicleItem.license_plate}</p>
        <img src="${URL.createObjectURL(vehicleItem.photo)}" alt="Foto del vehículo" style="width: 100px; margin: 5px;">
    `;

    vehicleList.appendChild(vehicleDiv);
    vehicles.push(vehicleItem); // Añadir el vehículo al array de la flota

    // Limpiar el formulario
    document.getElementById('vehicleForm').reset();
}

// Obtener el formulario y agregar el evento de submit para subir vehículos
document.getElementById('uploadVehiclesForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto del formulario

    if (vehicles.length === 0) {
        alert("No hay vehículos para subir.");
        return;
    }

    // Construir la URL para la subida de vehículos
    const url = '/api/post/create';

    // Enviar los datos al backend para crear el post
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(postInfo)
    })
    .then(response => {
        if (response.ok) {
            response.json().then(data => {
                // Asegúrate de que el `post_id` es un número entero
                const postId = data.post.post_id;
    
                if (!postId) {
                    throw new Error("post_id no encontrado.");
                }
    
                // Luego, para cada vehículo, enviar los datos con el `post_id` correcto
                vehicles.forEach(vehicle => {
                    const formData = new FormData();
                    formData.append('license_plate', vehicle.license_plate);
                    formData.append('brand', vehicle.brand);
                    formData.append('model', vehicle.model);
                    formData.append('registration_year', vehicle.registration_year);
                    formData.append('price', vehicle.price);
                    formData.append('observations', vehicle.observations);
                    formData.append('vehicle_type', vehicle.vehicleType);
                    formData.append('fuel_type', vehicle.fuelType);
                    formData.append('post_id', postId); // Aquí el `post_id` ya debería ser válido
                    formData.append('photo', vehicle.photo); // Ahora enviamos el archivo, no el base64

                    // Enviar los vehículos a la API
                    fetch('/api/vehicle/create', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            alert("Vehículo subido correctamente")
                            console.log("Vehicle uploaded successfully");
                        } else {
                            alert("Hubo un problema al subir el vehículo.");
                            console.error("Error uploading vehicle.");
                            throw new Error('Hubo un problema al crear el post.');
                        }
                    })
                    .catch(error => {
                        alert("Hubo un problema de red.");
                        console.error("Error de red:", error);
                    });
                });
                
                alert("Post creado correctamente");
                // Redirigir al usuario a la página de inicio
                window.location.href = '/img/home.html';
            });
        } else {
            throw new Error('Hubo un problema al crear el post.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema al crear el post.');
    });
});