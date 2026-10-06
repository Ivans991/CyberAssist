async function cargarActivos() {
    const respuesta = await fetch("/activos/", { cache: "no-store" });
    const activos = await respuesta.json();

    const tabla = document.getElementById("tabla-activos");
    tabla.innerHTML = "";

    activos.forEach(activo => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${activo.codigo}</td>
            <td>${activo.nombre}</td>
            <td>${activo.tipo}</td>
            <td>${activo.criticidad}</td>
            <td>${activo.estado}</td>
            <td>
                <button class="btn btn-sm btn-warning" onclick="cargarParaEditar(${activo.id})">Editar</button>
                <button class="btn btn-sm btn-danger" onclick="eliminarActivo(${activo.id})">Eliminar</button>
            </td>
        `;
        tabla.appendChild(fila);
    });
}

async function cargarParaEditar(id) {
    const respuesta = await fetch(`/activos/${id}`);
    const activo = await respuesta.json();

    const formulario = document.getElementById("form-activo");

    for (const campo in activo) {
        if (formulario.elements[campo]) {
            formulario.elements[campo].value = activo[campo] ?? "";
        }
    }

    document.getElementById("activo-id-editar").value = id;

    const boton = formulario.querySelector("button[type=submit]");
    boton.textContent = "Actualizar Activo";
    boton.classList.remove("btn-primary");
    boton.classList.add("btn-warning");

    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function eliminarActivo(id) {
    if (!confirm("¿Seguro que deseas eliminar este activo?")) {
        return;
    }

    const respuesta = await fetch(`/activos/${id}`, { method: "DELETE" });
    const mensaje = document.getElementById("mensaje");

    if (respuesta.ok) {
        mensaje.innerHTML = `<div class="alert alert-success">Activo eliminado correctamente.</div>`;
        cargarActivos();
    } else {
        const error = await respuesta.json();
        mensaje.innerHTML = `<div class="alert alert-danger">${error.detail}</div>`;
    }
}

document.getElementById("form-activo").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const formulario = evento.target;
    const datos = Object.fromEntries(new FormData(formulario).entries());
    const idEditando = document.getElementById("activo-id-editar").value;

    delete datos["activo-id-editar"];

    const url = idEditando ? `/activos/${idEditando}` : "/activos/";
    const metodo = idEditando ? "PUT" : "POST";

    const respuesta = await fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    });

    const mensaje = document.getElementById("mensaje");

    if (respuesta.ok) {
        mensaje.innerHTML = `<div class="alert alert-success">Activo ${idEditando ? "actualizado" : "creado"} correctamente.</div>`;
        formulario.reset();
        document.getElementById("activo-id-editar").value = "";

        const boton = formulario.querySelector("button[type=submit]");
        boton.textContent = "Crear Activo";
        boton.classList.remove("btn-warning");
        boton.classList.add("btn-primary");

        cargarActivos();
    } else {
        const error = await respuesta.json();
        mensaje.innerHTML = `<div class="alert alert-danger">Error: ${error.detail}</div>`;
    }
});

cargarActivos();