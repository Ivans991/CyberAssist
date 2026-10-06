async function cargarDashboard() {
    const respuesta = await fetch("/dashboard/");
    const datos = await respuesta.json();

    document.getElementById("total-activos").textContent = datos.total_activos;
    document.getElementById("total-vulnerabilidades").textContent = datos.total_vulnerabilidades;
    document.getElementById("riesgos-criticos").textContent = datos.riesgos_criticos;
    document.getElementById("riesgos-altos").textContent = datos.riesgos_altos;

    const totalRiesgos = datos.riesgos_criticos + datos.riesgos_altos + datos.riesgos_medios + datos.riesgos_bajos;
    const barra = document.getElementById("barra-riesgo");

    if (totalRiesgos === 0) {
        barra.innerHTML = `<div class="progress-bar bg-success" style="width: 100%">Sin riesgos activos</div>`;
        return;
    }

    const porcentaje = (valor) => (valor / totalRiesgos) * 100;

    barra.innerHTML = `
        <div class="progress-bar bg-danger" style="width: ${porcentaje(datos.riesgos_criticos)}%">
            ${datos.riesgos_criticos > 0 ? datos.riesgos_criticos : ""}
        </div>
        <div class="progress-bar bg-warning" style="width: ${porcentaje(datos.riesgos_altos)}%">
            ${datos.riesgos_altos > 0 ? datos.riesgos_altos : ""}
        </div>
        <div class="progress-bar bg-info" style="width: ${porcentaje(datos.riesgos_medios)}%">
            ${datos.riesgos_medios > 0 ? datos.riesgos_medios : ""}
        </div>
        <div class="progress-bar bg-success" style="width: ${porcentaje(datos.riesgos_bajos)}%">
            ${datos.riesgos_bajos > 0 ? datos.riesgos_bajos : ""}
        </div>
    `;
}

cargarDashboard();