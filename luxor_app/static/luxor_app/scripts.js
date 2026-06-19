/* Variables globales*/
 let cotizacionDolarOficial = 0;

 /**
 * API externa
 */

// Llamo a a la API apenas carga el sitio
fetch("/api/cotizacion-dolar/")
    .then(response => response.json())
    .then(data => {
        cotizacionDolarOficial = data.cotizacion;
        console.log(" Cotización obtenida desde el backend de Django: $" + cotizacionDolarOficial);

        if (data.status === 'fallback') {
            console.warn("El backend está sirviendo un valor de contingencia.");
        }
    })
    .catch(error => {
        console.error("Error al conectar con el endpoint interno de Django:", error);
    });

/**
 * Luxor APP
 */
document.addEventListener('DOMContentLoaded', () => {
    // Referencias al DOM
    const cards = document.querySelectorAll('.car-card');
    const selectedModelText = document.querySelector('.car-summary strong');
    const selectedPriceText = document.querySelector('.price-highlight');
    const selectedImage = document.querySelector('.informe-img');
    const sectionFinancimiento = document.querySelector('#financiamiento');
    const selectedModelo = document.getElementById('id_modelo');
    const formulario = document.getElementById('simulador-form');
    const comboModelo = document.getElementById('id_modelo');
    const comboPlan = document.getElementById('id_plan');
    const inputIngresoPersonal = document.getElementById('id_ingresos_personal');
    const cartelIngresoPersonal = document.getElementById('cartel-ingreso-personal');
    const inputIngresoGarante = document.getElementById('id_ingresos');
    const cartelIngresoGarante = document.getElementById('cartel-ingreso-garante');


    // Inicialización de Eventos de las Cards
    cards.forEach(card => {
        const btn = card.querySelector('.btn-select');

        btn.addEventListener('click', () => {
            // Deseleccionar previas y seleccionar actual
            updateCardSelection(cards, card);

            // Obtener datos de la card
            const modelName = card.getAttribute('data-model');
            const modelPrice = card.getAttribute('data-price');
            const carImageSrc = card.querySelector('.car-image img').getAttribute('src');

            // Actualizar Interfaz (Informe lateral y combo de datos del plan)
            updateSidebar(modelName, modelPrice, carImageSrc, {
                selectedModelText,
                selectedPriceText,
                selectedImage,
                selectedModelo
            });

            recalularSimulacion();

            // Scroll al formulario
            sectionFinancimiento.scrollIntoView({ behavior: 'smooth' });
        });
    });


    //Incialización de Seleccion de vehiculo
    if (comboModelo) {
        comboModelo.addEventListener('change', function() {
            const modeloSeleccionado = this.value;
            const infoAuto = document.querySelector('.car-card[data-model="'+modeloSeleccionado+'"]')

            updateCardSelection(cards, infoAuto);

            if (infoAuto) {
                updateSidebar(
                    modeloSeleccionado,
                    infoAuto.getAttribute('data-price'),
                    infoAuto.querySelector('.car-image img').getAttribute('src'),
                    {
                        selectedModelText,
                        selectedPriceText,
                        selectedImage
                    }
                );

                recalularSimulacion();
            }
        });
    }


    //Incialización de combo plan
    if (comboPlan) {
        comboPlan.addEventListener('change', function() {
            document.getElementById('dinamico-plan').innerText= comboPlan.value;
            reCalcular(null,null,null,null);
            recalularSimulacion();
        });
    }


    // --- EVENTOS DE VALIDACIÓN (BLUR E INPUT) ---

    // Nombre
    document.getElementById('id_nombre').addEventListener('blur', validarNombre);
    document.getElementById('id_nombre').addEventListener('input', () => {
        if (document.getElementById('id_nombre').value.trim().length >= 3) limpiarError('id_nombre');
    });

    // DNI
    document.getElementById('id_dni').addEventListener('blur', validarDni);
    document.getElementById('id_dni').addEventListener('input', () => {
        if (/^\d+$/.test(document.getElementById('id_dni').value.trim())) limpiarError('id_dni');
    });

    // Email
    document.getElementById('id_email').addEventListener('blur', validarEmail);
    document.getElementById('id_email').addEventListener('input', () => {
        const val = document.getElementById('id_email').value.trim();
        if (val.includes('@') && val.includes('.')) limpiarError('id_email');
    });

    // Ingresos Personal
    document.getElementById('id_ingresos_personal').addEventListener('blur', validarIngresos);
    document.getElementById('id_ingresos_personal').addEventListener('input', () => {
        const val = parseFloat(document.getElementById('id_ingresos_personal').value.trim());
        if (!isNaN(val) && val > 0) limpiarError('id_ingresos_personal');
    });

    // Ingresos Garante
    document.getElementById('id_ingresos').addEventListener('blur', validarIngresosGarante);
    document.getElementById('id_ingresos').addEventListener('input', () => {
        const val = parseFloat(document.getElementById('id_ingresos').value.trim());
        if (!isNaN(val) && val > 0) limpiarError('id_ingresos');
    });

    // Antigüedad Garante
    document.getElementById('id_garante_antiguedad').addEventListener('blur', validarAntiguedadGarante);
    document.getElementById('id_garante_antiguedad').addEventListener('input', () => {
        const val = parseInt(document.getElementById('id_garante_antiguedad').value.trim());
        if (!isNaN(val) && val > 0) limpiarError('id_garante_antiguedad');
    });


    // Formulario Submit
    if (formulario) {
        formulario.addEventListener('submit', function(event) {
            event.preventDefault();

            // Ejecuto todas las validaciones para pintar los errores
            const vNombre = validarNombre();
            const vDni = validarDni();
            const vEmail = validarEmail();
            const vIngresos = validarIngresos();
            const vIngresosG = validarIngresosGarante();
            const vAntiguedadG = validarAntiguedadGarante();
            const vTipoG = validarTipoGarante();

            // Si alguna falla, pongo foco a la pestaña correspondiente
            if (!vNombre || !vDni || !vEmail || !vIngresos) {
                const tab = document.querySelector('[onclick*="datos-personales"]');
                if (tab) tab.click();
                return;
            }
            if (!vIngresosG || !vAntiguedadG || !vTipoG) {
                const tab = document.querySelector('[onclick*="datos-garante"]');
                if (tab) tab.click();
                return;
            }


            // Envio de datos a django
            const datosParaEnviar = new FormData(formulario);
            document.getElementById("boton-simular").disabled = true;

            fetch('/simular-financiamiento/', {
                method: 'POST',
                body: datosParaEnviar,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) throw data;
                    document.getElementById("boton-simular").disabled = false;
                    return data;
                });
            })
            .then(data => {
                if (data.status === 'success') {
                    reCalcular( formatearPesos(data.resultado.adjudicacion),
                                formatearPesos(data.resultado.gastos_retiro),
                                data.resultado.tasa,
                                formatearPesos(data.resultado.cuota_mensual));

                    alert("¡Simulación procesada con éxito! Los datos fueron guardados y se ha enviado el informe por correo electrónico.");
                    document.getElementById("boton-simular").disabled = false;
                }
            })
            .catch(errorData => {
                let mensajeError = "El servidor rechazó los datos:\n";
                for (let campo in errorData.errors) {
                    mensajeError += `- ${errorData.errors[campo]}\n`;
                }
                alert(mensajeError);

                document.getElementById("boton-simular").disabled = false;
            });
        });
    }


    //Inicializo los carteles de conversion a dolares
    if (inputIngresoPersonal && cartelIngresoPersonal) {
        inputIngresoPersonal.addEventListener('input', function() {
            actualizarCartelDolar(inputIngresoPersonal, cartelIngresoPersonal);
        });
    }

    if (inputIngresoGarante && cartelIngresoGarante) {
        inputIngresoGarante.addEventListener('input', function() {
            actualizarCartelDolar(inputIngresoGarante, cartelIngresoGarante);
        });
    }
});

/**
 * Helpers
 */
// Maneja el estado visual de las tarjetas
function updateCardSelection(allCards, currentCard) {
    allCards.forEach(c => {
        c.classList.remove('selected');
        const btn = c.querySelector('.btn-select');
        if (btn) btn.innerText = "Seleccionar";
    });

    currentCard.classList.add('selected');
    currentCard.querySelector('.btn-select').innerText = "Seleccionado";
}

// Actualiza los elementos del resumen lateral
function updateSidebar(name, price, imgSrc, elements) {
    reCalcular(null,null,null,null);

    if (elements.selectedModelText) {
        elements.selectedModelText.innerText = name;
    }

    if (elements.selectedPriceText) {
        elements.selectedPriceText.innerText = `$${parseInt(price).toLocaleString('es-AR')}`;
    }

    if (elements.selectedImage) {
        elements.selectedImage.setAttribute('src', imgSrc);
    }

    if (elements.selectedModelo) {
        elements.selectedModelo.value=name;
    }
}

//Actualiza la simulacion en pantalla
function reCalcular(importes, gastoss, tasas, cuotas){
    const importeAdjudicacion=document.getElementById('dinamico-adjudicacion');
    const gastos=document.getElementById('dinamico-gastos');
    const tasa=document.getElementById('dinamico-tasa');
    const cuota=document.getElementById('dinamico-cuota-final');

   importeAdjudicacion.innerText = (importes) ? importes : "$ ----";
    gastos.innerText = (gastoss) ? gastoss : "$ ----";
    tasa.innerText = (tasas) ? tasas: "--,-- %";
    cuota.innerText = (cuotas) ? cuotas : "$ ----";
}

// Solicita la simulacion en caso que aplique
function recalularSimulacion(){
    if(   document.querySelector('input[name="garante_tipo_trabajo"]:checked')
       && document.getElementById('id_ingresos').value != ''
       && document.getElementById('id_ingresos_personal').value != ''
       && document.getElementById('id_garante_antiguedad').value > 0){

       // Evito que pida simulación automática si hay campos inválidos visibles en el DOM
       if (document.querySelectorAll('.is-invalid').length === 0) {
           document.getElementById('simulador-form').requestSubmit();
       }
    }
}

// Lógica de Tabs
function openTab(evt, tabName) {
    const tabPanels = document.querySelectorAll(".tab-panel");
    const tabBtns = document.querySelectorAll(".tab-btn");

    // Ocultar todos los paneles
    tabPanels.forEach(panel => {
        panel.style.display = "none";
        panel.classList.remove("active");
    });

    // Desactivar todos los botones
    tabBtns.forEach(btn => {
        btn.classList.remove("active");
    });

    // Activar panel y botón actual
    const targetTab = document.getElementById(tabName);
    if (targetTab) {
        targetTab.style.display = "block";
        targetTab.classList.add("active");
    }
    evt.currentTarget.classList.add("active");
}

// Función para mostrar el error
function mostrarError(idInput, mensaje) {
    const input = document.getElementById(idInput);
    if (!input) return;

    input.classList.add('is-invalid');

    // Si no ya existe el textito de error lo creo
    let errorSpan = input.parentElement.querySelector('.error-mensaje');
    if (!errorSpan) {
        errorSpan = document.createElement('span');
        errorSpan.className = 'error-mensaje';
        input.parentElement.appendChild(errorSpan);
    }
    errorSpan.innerText = mensaje;
}

// Funcion para limpiar el error
function limpiarError(idInput) {
    const input = document.getElementById(idInput);
    if (!input) return;

    input.classList.remove('is-invalid');
    const errorSpan = input.parentElement.querySelector('.error-mensaje');
    if (errorSpan) {
        errorSpan.remove();
    }
}

// Funciones de validación individuales por campo
function validarNombre() {
    const input = document.getElementById('id_nombre');
    if (input.value.trim().length < 3) {
        mostrarError('id_nombre', "El nombre debe tener al menos 3 caracteres.");
        return false;
    }
    limpiarError('id_nombre');
    return true;
}

function validarDni() {
    const input = document.getElementById('id_dni');
    const value = input.value.trim();
    const patronDni = /^\d+$/;

    if (value === "") {
        mostrarError('id_dni', "El DNI es obligatorio.");
        return false;
    }
    if (!patronDni.test(value)) {
        mostrarError('id_dni', "El DNI debe contener solo números, sin puntos ni guiones.");
        return false;
    }
    limpiarError('id_dni');
    return true;
}

function validarEmail() {
    const input = document.getElementById('id_email');
    const value = input.value.trim();
    if (value === "") {
        mostrarError('id_email', "El correo electrónico es obligatorio.");
        return false;
    }
    if (!value.includes('@') || !value.includes('.')) {
        mostrarError('id_email', "Ingrese un correo electrónico válido.");
        return false;
    }
    limpiarError('id_email');
    return true;
}

function validarIngresos() {
    const input = document.getElementById('id_ingresos_personal');
    const value = input.value.trim();
    if (value === "" || parseFloat(value) <= 0 || isNaN(parseFloat(value))) {
        mostrarError('id_ingresos_personal', "Los ingresos deben ser mayores a $0.");
        return false;
    }
    limpiarError('id_ingresos_personal');
    return true;
}

function validarIngresosGarante() {
    const input = document.getElementById('id_ingresos');
    const value = input.value.trim();
    if (value === "" || parseFloat(value) <= 0 || isNaN(parseFloat(value))) {
        mostrarError('id_ingresos', "Los ingresos del garante deben ser mayores a $0.");
        return false;
    }
    limpiarError('id_ingresos');
    return true;
}

function validarAntiguedadGarante() {
    const input = document.getElementById('id_garante_antiguedad');
    const value = input.value.trim();
    if (value === "" || parseInt(value) <= 0 || isNaN(parseInt(value))) {
        mostrarError('id_garante_antiguedad', "La antigüedad del garante debe ser mayor a 0.");
        return false;
    }
    limpiarError('id_garante_antiguedad');
    return true;
}

function validarTipoGarante(){
    // Este campo al ser radio buttons suele no requerir un textito abajo si la interfaz es clara,
    // pero mantenemos el alert global en el submit si no eligió ninguno para no romper la lógica actual.
    if(!document.querySelector('input[name="garante_tipo_trabajo"]:checked')){
        alert("Se debe especificar el tipo de relación de trabajo del garante.");
        return false;
    }
    return true;
}

// Funciones de formateo
function formatearPesos(numero) {
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(numero);
}

function formatearDolar(numero) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(numero);
}

// Funcion para actualizar el cartel de dolares
function actualizarCartelDolar(inputElement, cartelElement) {
    const valorEnPesos = parseFloat(inputElement.value);

   if (!valorEnPesos || isNaN(valorEnPesos) || cotizacionDolarOficial === 0) {
        cartelElement.innerText = "";
        return;
    }

    const equivalenciaDolares = valorEnPesos / cotizacionDolarOficial;

    const dolaresFormateados = formatearDolar(equivalenciaDolares);

    cartelElement.innerText = `Este importe equivale a u$s ${dolaresFormateados} bajo la cotización del dólar oficial del día ($${cotizacionDolarOficial}).`;
}