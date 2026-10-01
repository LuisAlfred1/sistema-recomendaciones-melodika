const CONFIGURACION_ALERTAS = {
  reabastecer_ya: {
    nombre: "Reabastecer ya",
    clase: "bg-red-100 text-red-800",
    prioridad: 0,
  },
  sin_inventario: {
    nombre: "Sin registro",
    clase: "bg-slate-200 text-slate-700",
    prioridad: 1,
  },
  cerca_del_minimo: {
    nombre: "Cerca del mínimo",
    clase: "bg-amber-100 text-amber-800",
    prioridad: 2,
  },
  ajustar_stock_maximo: {
    nombre: "Revisar máximo",
    clase: "bg-sky-100 text-sky-800",
    prioridad: 3,
  },
};

const PRODUCTOS_INVENTARIO_POR_PAGINA = 6;
let productosInventario = [];
let paginaInventarioActual = 1;

function escaparHTML(valor) {
  return String(valor ?? "").replace(/[&<>"']/g, (caracter) => {
    const entidades = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    };
    return entidades[caracter];
  });
}

function contarAlerta(tipo) {
  return productosInventario.filter((producto) =>
    producto.alertas.some((alerta) => alerta.tipo === tipo),
  ).length;
}

function actualizarResumen() {
  document.getElementById("conteo-reabastecer").textContent =
    contarAlerta("reabastecer_ya");
  document.getElementById("conteo-minimo").textContent =
    contarAlerta("cerca_del_minimo");
  document.getElementById("conteo-sin-inventario").textContent =
    contarAlerta("sin_inventario");
  document.getElementById("conteo-maximo").textContent = contarAlerta(
    "ajustar_stock_maximo",
  );
}

function obtenerEstadoPrincipal(alertas) {
  const alerta = [...alertas].sort(
    (a, b) =>
      (CONFIGURACION_ALERTAS[a.tipo]?.prioridad ?? 99) -
      (CONFIGURACION_ALERTAS[b.tipo]?.prioridad ?? 99),
  )[0];

  return alerta
    ? { ...CONFIGURACION_ALERTAS[alerta.tipo], tipo: alerta.tipo }
    : { nombre: "En rango", clase: "bg-emerald-100 text-emerald-800" };
}

function filtrarProductos() {
  const filtro = document.getElementById("filtro-inventario").value;
  if (filtro === "todos") return productosInventario;
  if (filtro === "atencion") {
    return productosInventario.filter(
      (producto) => producto.alertas.length > 0,
    );
  }

  return productosInventario.filter((producto) =>
    producto.alertas.some((alerta) => alerta.tipo === filtro),
  );
}

function renderizarInventario() {
  const tabla = document.getElementById("tabla-inventario");
  const resumen = document.getElementById("resumen-inventario");
  const filtro = document.getElementById("filtro-inventario");
  const visibles = filtrarProductos();
  const totalPaginas = Math.max(
    1,
    Math.ceil(visibles.length / PRODUCTOS_INVENTARIO_POR_PAGINA),
  );
  paginaInventarioActual = Math.min(paginaInventarioActual, totalPaginas);
  const inicio = (paginaInventarioActual - 1) * PRODUCTOS_INVENTARIO_POR_PAGINA;
  const productosPagina = visibles.slice(
    inicio,
    inicio + PRODUCTOS_INVENTARIO_POR_PAGINA,
  );
  const paginacion = document.getElementById("paginacion-inventario");

  if (visibles.length === 0) {
    tabla.innerHTML = `<tr><td colspan="6" class="px-4 py-8 text-center text-slate-500">No hay productos para este filtro.</td></tr>`;
    resumen.textContent = "0 productos";
    paginacion.classList.add("hidden");
    return;
  }

  tabla.innerHTML = productosPagina
    .map((producto) => {
      const estado = obtenerEstadoPrincipal(producto.alertas);
      const alertasSecundarias = producto.alertas.filter(
        (alerta) => alerta.tipo !== estado.tipo,
      );
      const etiquetas = alertasSecundarias.length
        ? alertasSecundarias
            .map((alerta) => {
              const config = CONFIGURACION_ALERTAS[alerta.tipo];
              if (!config) return "";
              return `<span class="mb-1 mr-1 inline-flex rounded px-2 py-1 text-xs font-semibold ${config.clase}">${config.nombre}</span>`;
            })
            .join("")
        : "";
      const recomendaciones = producto.alertas.length
        ? `<ul class="space-y-1 text-sm text-slate-600">${producto.alertas
            .map((alerta) => `<li>${escaparHTML(alerta.mensaje)}</li>`)
            .join("")}</ul>`
        : `<span class="text-sm text-slate-500">Sin acciones pendientes.</span>`;
      const stock = producto.inventario
        ? `<strong class="text-brand-dark">${producto.stock_actual}</strong>`
        : `<span class="text-sm font-medium text-slate-500">Sin registro</span>`;
      const accion = producto.inventario
        ? "Registrar entrada"
        : "Registrar stock";

      return `
        <tr class="align-top transition hover:bg-slate-50">
          <td class="px-4 py-4 font-medium text-brand-dark">${escaparHTML(producto.nombre)}</td>
          <td class="px-4 py-4">${stock}</td>
          <td class="px-4 py-4 text-slate-700">${producto.rotacion_30_dias} unidades</td>
          <td class="px-4 py-4"><span class="inline-flex rounded px-2 py-1 text-xs font-semibold ${estado.clase}">${estado.nombre}</span><div class="mt-2">${etiquetas}</div></td>
          <td class="max-w-sm px-4 py-4">${recomendaciones}</td>
          <td class="px-4 py-4"><button type="button" data-action="stock" data-id="${producto.id_producto}" class="whitespace-nowrap rounded-md bg-brand-purple px-3 py-2 text-xs font-semibold text-white transition hover:bg-brand-dark">${accion}</button></td>
        </tr>
      `;
    })
    .join("");

  resumen.textContent = `Mostrando ${inicio + 1}–${Math.min(inicio + PRODUCTOS_INVENTARIO_POR_PAGINA, visibles.length)} de ${visibles.length} productos`;
  document.getElementById("pagina-inventario-actual").textContent =
    `Página ${paginaInventarioActual} de ${totalPaginas}`;
  document.getElementById("inventario-pagina-anterior").disabled =
    paginaInventarioActual === 1;
  document.getElementById("inventario-pagina-siguiente").disabled =
    paginaInventarioActual === totalPaginas;
  paginacion.classList.toggle("hidden", totalPaginas <= 1);
  filtro.disabled = false;
}

async function cargarInventario() {
  const error = document.getElementById("mensaje-error-inventario");
  error.classList.add("hidden");

  try {
    const [productos, inventarios, recomendaciones] = await Promise.all([
      apiGet("/productos"),
      apiGet("/inventarios"),
      apiGet("/recomendaciones"),
    ]);
    const inventarioPorProducto = new Map(
      inventarios.map((inventario) => [inventario.id_producto, inventario]),
    );
    const recomendacionesPorProducto = new Map(
      recomendaciones.map((recomendacion) => [
        recomendacion.id_producto,
        recomendacion,
      ]),
    );

    productosInventario = productos
      .map((producto) => {
        const inventario = inventarioPorProducto.get(producto.id_producto);
        const recomendacion = recomendacionesPorProducto.get(
          producto.id_producto,
        );
        return {
          ...producto,
          inventario,
          stock_actual: inventario?.stock_actual ?? null,
          rotacion_30_dias: recomendacion?.rotacion_30_dias ?? 0,
          alertas: recomendacion?.alertas ?? [],
        };
      })
      .sort((a, b) => {
        const estadoA = obtenerEstadoPrincipal(a.alertas);
        const estadoB = obtenerEstadoPrincipal(b.alertas);
        return (estadoA.prioridad ?? 99) - (estadoB.prioridad ?? 99);
      });

    actualizarResumen();
    renderizarInventario();
  } catch (errorCarga) {
    error.textContent = `No se pudo cargar el inventario: ${errorCarga.message}`;
    error.classList.remove("hidden");
    document.getElementById("tabla-inventario").innerHTML =
      `<tr><td colspan="6" class="px-4 py-8 text-center text-slate-500">No se pudo cargar el inventario.</td></tr>`;
  }
}

const modalStock = document.getElementById("modal-stock");
const formularioStock = document.getElementById("form-stock");

function abrirModalStock(idProducto) {
  const producto = productosInventario.find(
    (item) => String(item.id_producto) === String(idProducto),
  );
  if (!producto) return;

  const esEntrada = Boolean(producto.inventario);
  const cantidad = formularioStock.elements.namedItem("cantidad");
  formularioStock.reset();
  formularioStock.elements.namedItem("id_producto").value =
    producto.id_producto;
  formularioStock.elements.namedItem("id_inventario").value =
    producto.inventario?.id_inventario ?? "";
  document.getElementById("titulo-modal-stock").textContent = esEntrada
    ? "Registrar entrada"
    : "Registrar stock inicial";
  document.getElementById("nombre-modal-stock").textContent = producto.nombre;
  document.getElementById("etiqueta-cantidad-stock").textContent = esEntrada
    ? "Unidades recibidas"
    : "Stock actual inicial";

  const disponible = Math.max(
    0,
    producto.stock_maximo - (producto.stock_actual ?? 0),
  );
  cantidad.max = disponible;
  document.getElementById("ayuda-stock").textContent = esEntrada
    ? `Stock actual: ${producto.stock_actual}. Puedes recibir hasta ${disponible} unidades para no superar el máximo de ${producto.stock_maximo}.`
    : `El máximo permitido para este producto es ${producto.stock_maximo} unidades.`;
  document.getElementById("error-modal-stock").classList.add("hidden");
  modalStock.showModal();
  cantidad.focus();
}

document.getElementById("filtro-inventario").addEventListener("change", () => {
  paginaInventarioActual = 1;
  renderizarInventario();
});

document
  .getElementById("inventario-pagina-anterior")
  .addEventListener("click", () => {
    if (paginaInventarioActual > 1) {
      paginaInventarioActual -= 1;
      renderizarInventario();
    }
  });

document
  .getElementById("inventario-pagina-siguiente")
  .addEventListener("click", () => {
    const totalPaginas = Math.ceil(
      filtrarProductos().length / PRODUCTOS_INVENTARIO_POR_PAGINA,
    );
    if (paginaInventarioActual < totalPaginas) {
      paginaInventarioActual += 1;
      renderizarInventario();
    }
  });

document
  .getElementById("tabla-inventario")
  .addEventListener("click", (evento) => {
    const boton = evento.target.closest('button[data-action="stock"]');
    if (boton) abrirModalStock(boton.dataset.id);
  });

document.querySelectorAll("[data-cerrar-stock]").forEach((boton) => {
  boton.addEventListener("click", () => modalStock.close());
});

formularioStock.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const idProducto = formularioStock.elements.namedItem("id_producto").value;
  const idInventario =
    formularioStock.elements.namedItem("id_inventario").value;
  const cantidad = Number(formularioStock.elements.namedItem("cantidad").value);
  const producto = productosInventario.find(
    (item) => String(item.id_producto) === String(idProducto),
  );
  const stockNuevo = (producto?.stock_actual ?? 0) + cantidad;

  if (!producto || cantidad <= 0 || stockNuevo > producto.stock_maximo) {
    const error = document.getElementById("error-modal-stock");
    error.textContent = `La cantidad debe ser mayor que cero y el stock total no puede superar ${producto?.stock_maximo ?? 0}.`;
    error.classList.remove("hidden");
    return;
  }

  const boton = formularioStock.querySelector('button[type="submit"]');
  boton.disabled = true;
  try {
    if (idInventario) {
      await apiPost(`/inventarios/${idInventario}/entrada`, { cantidad });
    } else {
      await apiPost("/inventarios", {
        id_producto: Number(idProducto),
        stock_actual: cantidad,
      });
    }
    modalStock.close();
    await cargarInventario();
  } catch (error) {
    const mensaje = document.getElementById("error-modal-stock");
    mensaje.textContent = error.message;
    mensaje.classList.remove("hidden");
  } finally {
    boton.disabled = false;
  }
});

document.addEventListener("DOMContentLoaded", cargarInventario);
