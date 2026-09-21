from flask import Blueprint, jsonify, request
from models import db, Venta, DetalleVenta, Producto, Inventario

venta_bp = Blueprint("venta", __name__, url_prefix="/api/ventas")

@venta_bp.get("")
def listar_ventas():
    ventas = Venta.query.all()
    return jsonify([v.to_dict() for v in ventas])

@venta_bp.get("/<int:id_venta>")
def obtener_venta(id_venta):
    venta = Venta.query.get_or_404(id_venta)
    return jsonify(venta.to_dict())

@venta_bp.post("")
def crear_venta():
    """
    Body esperado:
    {
        "id_cliente": 1,
        "id_empleado": 2,
        "detalles": [
            {"id_producto": 5, "cantidad": 3},
            {"id_producto": 7, "cantidad": 1}
        ]
    }
    El precio_unitario y subtotal de cada detalle, y el total de la venta,
    se calculan aquí — nunca vienen del cliente.
    """
    data = request.get_json()
    detalles_data = data.get("detalles", [])

    if not detalles_data:
        return jsonify({"error": "La venta debe incluir al menos un detalle"}), 400

    try:
        venta = Venta(
            id_cliente=data["id_cliente"],
            id_empleado=data["id_empleado"],
            total=0,
        )
        db.session.add(venta)
        db.session.flush()  # asigna id_venta sin hacer commit todavía

        total_venta = 0

        for item in detalles_data:
            producto = Producto.query.get(item["id_producto"])
            if producto is None:
                raise ValueError(f"El producto {item['id_producto']} no existe")

            cantidad = item["cantidad"]

            inventario = Inventario.query.filter_by(id_producto=producto.id_producto).first()
            if inventario is None or inventario.stock_actual < cantidad:
                raise ValueError(f"Stock insuficiente para el producto '{producto.nombre}'")

            precio_unitario = producto.precio_unitario
            subtotal = cantidad * precio_unitario

            detalle = DetalleVenta(
                id_venta=venta.id_venta,
                id_producto=producto.id_producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal,
            )
            db.session.add(detalle)

            inventario.stock_actual -= cantidad
            total_venta += subtotal

        venta.total = total_venta
        db.session.commit()

        return jsonify(venta.to_dict()), 201

    except (KeyError, ValueError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400