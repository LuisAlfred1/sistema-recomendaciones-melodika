const PRODUCTOS_POR_PAGINA = 6;
let productos = [];
let paginaActual = 1;

function renderizarProductos() {
  const tabla = document.getElementById("tabla-productos");
  const totalPaginas = Math.max(
    1,
    Math.ceil(productos.length / PRODUCTOS_POR_PAGINA),
  );
  paginaActual = Math.min(paginaActual, totalPaginas);

  const inicio = (paginaActual - 1) * PRODUCTOS_POR_PAGINA;
  const productosPagina = productos.slice(
    inicio,
    inicio + PRODUCTOS_POR_PAGINA,
  );
  const navPaginacion = document.getElementById("paginacion-productos");
  const resumen = document.getElementById("resumen-paginacion");

  if (productos.length === 0) {
    tabla.innerHTML = `<tr><td colspan="6" class="px-5 py-8 text-center text-slate-500">No hay productos todavía</td></tr>`;
    resumen.textContent = "0 productos";
    navPaginacion.classList.add("hidden");
    return;
  }

  tabla.innerHTML = productosPagina
    .map(
      (p) => `
        <tr class="transition hover:bg-slate-50">
          <td class="px-5 py-3 text-slate-500">${p.id_producto}</td>
          <td class="px-5 py-3 font-medium text-brand-dark">${p.nombre}</td>
          <td class="px-5 py-3">Q${Number(p.precio_unitario).toFixed(2)}</td>
          <td class="px-5 py-3">${p.stock_minimo}</td>
          <td class="px-5 py-3">${p.stock_maximo}</td>
          <td class="whitespace-nowrap px-5 py-3">
            <button type="button" data-action="edit" data-id="${p.id_producto}" class="mr-2 rounded-md bg-brand-purple px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-brand-dark">Editar</button>
            <button type="button" data-action="delete" data-id="${p.id_producto}" class="rounded-md border border-red-200 px-3 py-1.5 text-xs font-semibold text-red-700 transition hover:bg-red-50">Eliminar</button>
          </td>
        </tr>
        `,
    )
    .join("");

  resumen.textContent = `Mostrando ${inicio + 1}–${Math.min(inicio + PRODUCTOS_POR_PAGINA, productos.length)} de ${productos.length} productos`;
  document.getElementById("pagina-actual").textContent =
    `Página ${paginaActual} de ${totalPaginas}`;
  document.getElementById("pagina-anterior").disabled = paginaActual === 1;
  document.getElementById("pagina-siguiente").disabled =
    paginaActual === totalPaginas;
  navPaginacion.classList.toggle("hidden", totalPaginas <= 1);
}

async function cargarProductos() {
  try {
    productos = await apiGet("/productos");
    renderizarProductos();
  } catch (error) {
    mostrarError(error.message);
  }
}

function mostrarError(mensaje) {
  const caja = document.getElementById("mensaje-error");
  caja.textContent = mensaje;
  caja.classList.remove("hidden");
}

function ocultarError() {
  document.getElementById("mensaje-error").classList.add("hidden");
}

const modalProducto = document.getElementById("modal-producto");
const modalEliminar = document.getElementById("modal-eliminar");
const formularioProducto = document.getElementById("form-producto");

function ocultarErrorModal(id) {
  document.getElementById(id).classList.add("hidden");
}

function mostrarErrorModal(id, mensaje) {
  const error = document.getElementById(id);
  error.textContent = mensaje;
  error.classList.remove("hidden");
}

function abrirModalCrear() {
  formularioProducto.reset();
  formularioProducto.elements.namedItem("id_producto").value = "";
  document.getElementById("titulo-modal-producto").textContent =
    "Crear producto";
  document.getElementById("boton-guardar-producto").textContent =
    "Crear producto";
  ocultarErrorModal("error-modal-producto");
  ocultarError();
  modalProducto.showModal();
  formularioProducto.elements.namedItem("nombre").focus();
}

async function editarProducto(id) {
  ocultarError();

  try {
    const producto = await apiGet(`/productos/${id}`);
    formularioProducto.elements.namedItem("id_producto").value =
      producto.id_producto;
    formularioProducto.elements.namedItem("nombre").value = producto.nombre;
    formularioProducto.elements.namedItem("id_categoria").value =
      producto.id_categoria;
    formularioProducto.elements.namedItem("id_proveedor").value =
      producto.id_proveedor;
    formularioProducto.elements.namedItem("precio_unitario").value =
      producto.precio_unitario;
    formularioProducto.elements.namedItem("stock_minimo").value =
      producto.stock_minimo;
    formularioProducto.elements.namedItem("stock_maximo").value =
      producto.stock_maximo;
    document.getElementById("titulo-modal-producto").textContent =
      "Editar producto";
    document.getElementById("boton-guardar-producto").textContent =
      "Guardar cambios";
    ocultarErrorModal("error-modal-producto");
    modalProducto.showModal();
    formularioProducto.elements.namedItem("nombre").focus();
  } catch (error) {
    mostrarError(error.message);
  }
}

async function prepararEliminacion(id) {
  ocultarError();
  try {
    const producto = await apiGet(`/productos/${id}`);
    document.getElementById("nombre-producto-eliminar").textContent =
      `${producto.nombre} (ID ${producto.id_producto})`;
    document.getElementById("confirmar-eliminar").dataset.id =
      producto.id_producto;
    ocultarErrorModal("error-modal-eliminar");
    modalEliminar.showModal();
  } catch (error) {
    mostrarError(error.message);
  }
}

async function eliminarProducto() {
  const boton = document.getElementById("confirmar-eliminar");
  boton.disabled = true;
  try {
    await apiDelete(`/productos/${boton.dataset.id}`);
    modalEliminar.close();
    await cargarProductos();
  } catch (error) {
    mostrarErrorModal("error-modal-eliminar", error.message);
  } finally {
    boton.disabled = false;
  }
}

document
  .getElementById("abrir-modal-crear")
  .addEventListener("click", abrirModalCrear);

document.querySelectorAll("[data-cerrar-producto]").forEach((boton) => {
  boton.addEventListener("click", () => modalProducto.close());
});

document.querySelectorAll("[data-cerrar-eliminar]").forEach((boton) => {
  boton.addEventListener("click", () => modalEliminar.close());
});

modalProducto.addEventListener("close", () => {
  formularioProducto.reset();
  formularioProducto.elements.namedItem("id_producto").value = "";
});

document
  .getElementById("tabla-productos")
  .addEventListener("click", (evento) => {
    const boton = evento.target.closest("button[data-action]");
    if (!boton) return;

    const { action, id } = boton.dataset;
    if (action === "edit") editarProducto(id);
    if (action === "delete") prepararEliminacion(id);
  });

document.getElementById("pagina-anterior").addEventListener("click", () => {
  if (paginaActual > 1) {
    paginaActual -= 1;
    renderizarProductos();
  }
});

document.getElementById("pagina-siguiente").addEventListener("click", () => {
  const totalPaginas = Math.ceil(productos.length / PRODUCTOS_POR_PAGINA);
  if (paginaActual < totalPaginas) {
    paginaActual += 1;
    renderizarProductos();
  }
});

document
  .getElementById("confirmar-eliminar")
  .addEventListener("click", eliminarProducto);

document
  .getElementById("form-producto")
  .addEventListener("submit", async (evento) => {
    evento.preventDefault();
    ocultarError();

    const formulario = evento.target;
    const datos = {
      nombre: formulario.nombre.value,
      id_categoria: Number(formulario.id_categoria.value),
      id_proveedor: Number(formulario.id_proveedor.value),
      precio_unitario: Number(formulario.precio_unitario.value),
      stock_minimo: Number(formulario.stock_minimo.value),
      stock_maximo: Number(formulario.stock_maximo.value),
    };

    try {
      const id = formulario.elements.namedItem("id_producto").value;
      if (id) {
        await apiPut(`/productos/${id}`, datos);
      } else {
        await apiPost("/productos", datos);
        paginaActual = 1;
      }
      modalProducto.close();
      await cargarProductos();
    } catch (error) {
      mostrarErrorModal("error-modal-producto", error.message);
    }
  });

document.addEventListener("DOMContentLoaded", cargarProductos);
