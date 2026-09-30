const COLOR_POR_TIPO = {
  reabastecer_ya: "bg-red-100 text-red-800",
  cerca_del_minimo: "bg-amber-100 text-amber-800",
  ajustar_stock_maximo: "bg-sky-100 text-sky-800",
  sin_inventario: "bg-slate-200 text-slate-700",
};

function crearTarjeta(item) {
  const badges = item.alertas
    .map(
      (a) =>
        `<span class="mr-1 inline-flex rounded px-2 py-1 text-xs font-semibold ${COLOR_POR_TIPO[a.tipo] || "bg-slate-200 text-slate-700"}">${a.tipo}</span>`,
    )
    .join("");

  const mensajes = item.alertas.map((a) => `<li>${a.mensaje}</li>`).join("");

  return `
        <article class="rounded-lg border border-slate-200 border-l-4 border-l-brand-gold bg-white p-5 shadow-sm">
            <h2 class="text-base font-semibold text-brand-dark">${item.nombre}</h2>
            <p class="mt-3">${badges}</p>
            <p class="mt-3 text-sm text-slate-600">Stock actual: <strong class="text-brand-dark">${item.stock_actual ?? "N/D"}</strong></p>
            <p class="mt-1 text-sm text-slate-600">Rotación (30 días): <strong class="text-brand-dark">${item.rotacion_30_dias}</strong></p>
            <ul class="mt-3 space-y-1 text-sm text-slate-500">${mensajes}</ul>
        </article>
    `;
}

async function cargarRecomendaciones() {
  const contenedor = document.getElementById("contenedor-recomendaciones");
  try {
    const recomendaciones = await apiGet("/recomendaciones");

    if (recomendaciones.length === 0) {
      contenedor.innerHTML = `<p class="rounded-md border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800 lg:col-span-2 2xl:col-span-3">Sin alertas por el momento. Todo el inventario está en buen estado.</p>`;
      return;
    }

    contenedor.innerHTML = recomendaciones.map(crearTarjeta).join("");
  } catch (error) {
    contenedor.innerHTML = `<p class="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-800 lg:col-span-2 2xl:col-span-3">No se pudieron cargar las recomendaciones: ${error.message}</p>`;
  }
}

document.addEventListener("DOMContentLoaded", cargarRecomendaciones);
