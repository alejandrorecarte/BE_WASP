window.onload = function () {
    verificarSesion();
    const cardsSection = document.getElementById('cardsSection');
    const params = new URLSearchParams(window.location.search);
    let page = parseInt(params.get('page')); 
    if (page === null || isNaN(page) || page < 1) {
        page = 1;
    }

    // Cargar las tarjetas al cargar la página
    loadCards(cardsSection, page);
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

document.addEventListener('DOMContentLoaded', function () {
    console.log("Adding event listeners")

    document.getElementById("addPostButton").addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = '/img/createPost.html';  // Asegúrate de que la ruta sea la correcta
    });

    document.getElementById("logoutButton").addEventListener("click", function () {
        fetch('/api/users/logout', {
            method: 'POST'
        })
            .then(response => {
                if (response.ok) {
                    // Si la respuesta es OK (status 200), el token es válido
                    console.log("Session Closed")
                    window.location.href = '../index.html';  // Asegúrate de que la ruta sea la correcta
                } else {
                    console.log("Session not closed")
                    alert("No se pudo cerrar la sesión")
                }
            })
            .catch(error => {
                console.error('Error al verificar la sesión:', error);
                mostrarBotonesLoginRegistro(authButtons);  // Si hay un error, mostrar los botones de login y registro
            });
    })
});


// Función para crear una tarjeta
function createCard(title, description, postId) {
    const card = document.createElement('div');
    card.className = 'card';
    card.addEventListener('click', () => {
        window.location.href = `post.html?post_id=${postId}`; // Redirigir a post.html con el id del post
    });

    const cardTitle = document.createElement('h2');
    cardTitle.textContent = title;

    const cardDescription = document.createElement('p');
    cardDescription.textContent = description;

    card.appendChild(cardTitle);
    card.appendChild(cardDescription);

    return card;
}


function loadCards(cardsSection, page) {
    page--
    console.log("Cargando tarjetas de la página:", page);
    const url = `/api/post/last?page=${page}`; // Construir la URL con el parámetro page
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("Llamada la API exitosa.")
            cardsSection.innerHTML = '';
            data.last_posts.forEach(item => {
                console.log("Creando tarjeta para:", item.title);
                const card = createCard(item.title, item.description, item.post_id);
                cardsSection.appendChild(card);
            });
            generatePaginationControls(data.page, data.max_pages);
        })
        .catch(error => console.error('Error al cargar las tarjetas:', error));
}

   // Función para generar los controles de paginación
   function generatePaginationControls(currentPage, maxPages) {
    console.log("Generando controles de paginación..." + currentPage + " " + maxPages);
    const paginationControls = document.getElementById('paginationControls');
    paginationControls.innerHTML = '';

    for (let i = 1; i <= maxPages; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        button.className = 'pagination-button';
        if (i === currentPage) {
            button.disabled = true;
        }
        button.addEventListener('click', function() { 
            window.location.href = `/img/home.html?page=${i}`;
        });
        paginationControls.appendChild(button); // Asegúrate de agregar el botón al contenedor
    }
}