const csrftoken = Cookies.get('csrftoken');
const ATRIBUTO_ACTIVO = "data-activo";


function post(url, callback) {
    var request = new Request(url);

    fetch(request, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    }).then(response => callback(response));
}

function hacerPostASubDominioDeVotosYActualizarPuntos(subdominio, idSolucion, onSuccess) {
    post(
        '/soluciones/' + idSolucion + '/votos/' + subdominio + '/',
        response => {
            if (response.status === 200) {
                const puntosElement = document.getElementById('puntos-' + idSolucion);
                const puntos = response.headers.get('Puntos');
                puntosElement.innerHTML = puntos;
                onSuccess();
            }
        }
    );
}

function activarFlecha(flecha) {
    flecha.style.removeProperty("color");
    flecha.classList.add("text-primary");
    flecha.setAttribute(ATRIBUTO_ACTIVO, "");
}

function desactivarFlecha(flecha) {
    flecha.classList.remove("text-primary");
    flecha.style.color = "lightgrey";
    flecha.removeAttribute(ATRIBUTO_ACTIVO);
}

function cambiarColores(desactivado, activado) {
    desactivarFlecha(desactivado);
    activarFlecha(activado);
}

function sacarVoto(idSolucion, elementoDesactivado) {
    hacerPostASubDominioDeVotosYActualizarPuntos(
        'sacar', idSolucion, () => desactivarFlecha(elementoDesactivado));
}

function apretarFlecha(idSolucion, flechaApretada, otraFlecha, subdominio) {
    if (flechaApretada.hasAttribute(ATRIBUTO_ACTIVO)) {
        sacarVoto(idSolucion, flechaApretada);
    } else {
        hacerPostASubDominioDeVotosYActualizarPuntos(
            subdominio, idSolucion, () => cambiarColores(otraFlecha, flechaApretada));
    }
}

function apretarFlechaArriba(idSolucion) {
    const votarAbajo = document.getElementById('votar-abajo-' + idSolucion);
    const votarArriba = document.getElementById('votar-arriba-' + idSolucion);
    apretarFlecha(idSolucion, votarArriba, votarAbajo, 'arriba');
}

function apretarFlechaAbajo(idSolucion) {
    const votarAbajo = document.getElementById('votar-abajo-' + idSolucion);
    const votarArriba = document.getElementById('votar-arriba-' + idSolucion);
    const puntosElement = document.getElementById('puntos-' + idSolucion);
    const puntos = parseInt(puntosElement.innerHTML);
    const abajoActivo = votarAbajo.hasAttribute(ATRIBUTO_ACTIVO);
    const arribaActivo = votarArriba.hasAttribute(ATRIBUTO_ACTIVO);
    if (abajoActivo || puntos >= 2 || (!arribaActivo && puntos >= 1)) {
        apretarFlecha(idSolucion, votarAbajo, votarArriba, 'abajo');
    }
}