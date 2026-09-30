from datetime import datetime, timedelta

from flask import Blueprint, jsonify
from sqlalchemy import func

from models import db, Producto, Inventario, DetalleVenta, Venta

# Blueprint para las rutas de recomendación
recomendacion_bp = Blueprint("recomendacion", __name__, url_prefix="/api/recomendaciones")

DIAS_ROTACION = 30
MARGEN_ADVERTENCIA = 1.3  # 30% por encima del mínimo se considera "cerca del mínimo"

# Función para calcular la rotación de un producto en los últimos 30 días
def calcular_rotacion(id_producto, desde):
    
    # Unidades vendidas de un producto desde la fecha indicada.
    resultado = (
        #Consulta SQL para sumar la cantidad de unidades vendidas del producto en los últimos 30 días.
        # Se utiliza la función coalesce para devolver 0 si no hay ventas registradas.
        db.session.query(func.coalesce(func.sum(DetalleVenta.cantidad), 0))
        # Se realiza un join entre las tablas DetalleVenta y Venta para obtener las ventas correspondientes al producto.
        .join(Venta, DetalleVenta.id_venta == Venta.id_venta)
        # Se filtra por el id del producto y la fecha de venta mayor o igual a la fecha indicada (desde).
        .filter(DetalleVenta.id_producto == id_producto, Venta.fecha_venta >= desde)
        # Se obtiene el resultado de la consulta como un valor escalar (un solo valor).
        .scalar()
    )
    return int(resultado)

# Función para evaluar el estado de un producto y generar alertas según su inventario y rotación
def evaluar_producto(producto, inventario, rotacion):
    # Se inicializa una lista de alertas vacía para almacenar las recomendaciones generadas.
    alertas = []

    # Se obtiene el stock actual del inventario si existe, de lo contrario se establece en 0.
    stock_actual = inventario.stock_actual if inventario else 0

    if inventario is None:
        alertas.append({
            "tipo": "sin_inventario",
            "mensaje": "Este producto no tiene un registro de inventario asociado",
        })
    elif stock_actual < producto.stock_minimo:
        alertas.append({
            "tipo": "reabastecer_ya",
            "mensaje": f"Stock actual ({stock_actual}) está por debajo del mínimo ({producto.stock_minimo})",
        })
    elif stock_actual <= producto.stock_minimo * MARGEN_ADVERTENCIA:
        # Ejemplo: Si el stock minimo es de 10, y el margen de advertencia es 1.3, entonces si el stock actual es menor o igual a 13 (10 * 1.3), se considera "cerca del mínimo".
        alertas.append({
            "tipo": "cerca_del_minimo",
            "mensaje": f"Stock actual ({stock_actual}) se está acercando al mínimo ({producto.stock_minimo})",
        })

    # Para que la recomendacion aplique, se debe haber vendido al menos una unidad en los últimos 30 días.
    if rotacion > 0 and rotacion > producto.stock_maximo:
        alertas.append({
            "tipo": "ajustar_stock_maximo",
            "mensaje": (
                f"Se vendieron {rotacion} unidades en los últimos {DIAS_ROTACION} días, "
                f"superando el stock máximo actual ({producto.stock_maximo}). "
                f"Considera subirlo."
            ),
        })
    
    return alertas

@recomendacion_bp.get("")
def listar_recomendaciones():
    # Se calcula la fecha desde la cual se evaluará la rotación de los productos (30 días atrás).
    desde = datetime.utcnow() - timedelta(days=DIAS_ROTACION)
    # Se obtienen todos los productos de la base de datos.
    productos = Producto.query.all()

    recomendaciones = []
    # Se itera sobre cada producto para evaluar su estado y generar recomendaciones.
    for producto in productos:
        # Se obtiene el registro de inventario correspondiente al producto.
        inventario = Inventario.query.filter_by(id_producto=producto.id_producto).first()
        # Se calcula la rotación del producto en los últimos 30 días.
        rotacion = calcular_rotacion(producto.id_producto, desde)
        # Se evalúa el producto para determinar si hay alertas basadas en su inventario y rotación.
        alertas = evaluar_producto(producto, inventario, rotacion)

        # Si hay alertas, se agrega la información del producto y las alertas a la lista de recomendaciones.
        if alertas:
            recomendaciones.append({
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "stock_actual": inventario.stock_actual if inventario else None,
                "stock_minimo": producto.stock_minimo,
                "stock_maximo": producto.stock_maximo,
                "rotacion_30_dias": rotacion,
                "alertas": alertas,
            })

    return jsonify(recomendaciones)

# Ruta para obtener recomendaciones específicas de un producto por su ID
@recomendacion_bp.get("/<int:id_producto>")
def recomendacion_de_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    inventario = Inventario.query.filter_by(id_producto=id_producto).first()
    desde = datetime.utcnow() - timedelta(days=DIAS_ROTACION)
    rotacion = calcular_rotacion(id_producto, desde)
    alertas = evaluar_producto(producto, inventario, rotacion)

    return jsonify({
        "id_producto": producto.id_producto,
        "nombre": producto.nombre,
        "stock_actual": inventario.stock_actual if inventario else None,
        "stock_minimo": producto.stock_minimo,
        "stock_maximo": producto.stock_maximo,
        "rotacion_30_dias": rotacion,
        "alertas": alertas,
    })