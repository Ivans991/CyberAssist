let mapaActivos = {};

async function cargarActivosEnSelect() {
    const respuesta = await fetch("/activos/");
    const activos = await respuesta.json();

    const select = document.getElementById("select-activo");
    select.innerHTML = '<option value="">Selecciona un activo...</option>';

    activos.forEach(activo => {
        mapaActivos[activo.id] = `${activo.codigo} - ${activo.nombre}`;
        const opcion = document.createElement("option");
        opcion.value = activo.id;
        opcion.textContent = `${activo.codigo} - ${activo.nombre}`;
        select.appendChild(opcion);
    });
}

async function cargarVulnerabilidades() {
    const respuesta = await fetch("/vulnerabilidades/");
    const vulnerabilidades = await respuesta.json();

    const tabla = document.getElementById("tabla-vulnerabilidades");
    tabla.innerHTML = "";

    vulnerabilidades.forEach(v => {
        const nombreActivo = mapaActivos[v.activo_id] || `Activo #${v.activo_id}`;
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${nombreActivo}</td>
            <td>${v.nombre}</td>
            <td>${v.severidad}</td>
            <td>${v.riesgo}</td>
            <td>${v.recomendacion}</td>
            <td>${v.estado}</td>
            <td>
                <button class="btn btn-sm btn-warning" onclick="cargarParaEditar(${v.id})">Editar</button>
                <button class="btn btn-sm btn-danger" onclick="eliminarVulnerabilidad(${v.id})">Eliminar</button>
            </td>
        `;
        tabla.appendChild(fila);
    });
}

async function cargarParaEditar(id) {
    const respuesta = await fetch(`/vulnerabilidades/${id}`);
    const vulnerabilidad = await respuesta.json();

    const formulario = document.getElementById("form-vulnerabilidad");

    for (const campo in vulnerabilidad) {
        if (formulario.elements[campo]) {
            formulario.elements[campo].value = vulnerabilidad[campo] ?? "";
        }
    }

    document.getElementById("vulnerabilidad-id-editar").value = id;

    const boton = formulario.querySelector("button[type=submit]");
    boton.textContent = "Actualizar Vulnerabilidad";
    boton.classList.remove("btn-primary");
    boton.classList.add("btn-warning");

    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function eliminarVulnerabilidad(id) {
    if (!confirm("¿Seguro que deseas eliminar esta vulnerabilidad?")) {
        return;
    }

    const respuesta = await fetch(`/vulnerabilidades/${id}`, { method: "DELETE" });
    const mensaje = document.getElementById("mensaje");

    if (respuesta.ok) {
        mensaje.innerHTML = `<div class="alert alert-success">Vulnerabilidad eliminada correctamente.</div>`;
        cargarVulnerabilidades();
    } else {
        const error = await respuesta.json();
        mensaje.innerHTML = `<div class="alert alert-danger">${error.detail}</div>`;
    }
}

document.getElementById("form-vulnerabilidad").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const formulario = evento.target;
    const datos = Object.fromEntries(new FormData(formulario).entries());
    const idEditando = document.getElementById("vulnerabilidad-id-editar").value;

    if (idEditando) {
        delete datos.activo_id;
    } else {
        datos.activo_id = parseInt(datos.activo_id);
    }

    const url = idEditando ? `/vulnerabilidades/${idEditando}` : "/vulnerabilidades/";
    const metodo = idEditando ? "PUT" : "POST";

    const respuesta = await fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    });

    const mensaje = document.getElementById("mensaje");

    if (respuesta.ok) {
        mensaje.innerHTML = `<div class="alert alert-success">Vulnerabilidad ${idEditando ? "actualizada" : "registrada"} correctamente.</div>`;
        formulario.reset();
        document.getElementById("vulnerabilidad-id-editar").value = "";

        const boton = formulario.querySelector("button[type=submit]");
        boton.textContent = "Registrar Vulnerabilidad";
        boton.classList.remove("btn-warning");
        boton.classList.add("btn-primary");

        cargarVulnerabilidades();
    } else {
        const error = await respuesta.json();
        mensaje.innerHTML = `<div class="alert alert-danger">Error: ${error.detail}</div>`;
    }
});

cargarActivosEnSelect().then(cargarVulnerabilidades);