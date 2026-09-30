from datetime import datetime
from flask import Blueprint, jsonify, request
from models import db, Inventario, Producto

inventario_bp = Blueprint("inventario", __name__, url_prefix="/api/inventarios")

@inventario_bp.get("")
def listar_inventarios():
    inventarios = Inventario.query.all()
    return jsonify([i.to_dict() for i in inventarios])

@inventario_bp.get("/<int:id_inventario>")
def obtener_inventario(id_inventario):
    inventario = Inventario.query.get_or_404(id_inventario)
    return jsonify(inventario.to_dict())

@inventario_bp.post("")
def crear_inventario():
    data = request.get_json()
    nuevo = Inventario(
        id_producto=data["id_producto"],
        stock_actual=data.get("stock_actual", 0),
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201

@inventario_bp.put("/<int:id_inventario>")
def actualizar_inventario(id_inventario):
    """Ajuste absoluto del stock (ej. corrección por conteo físico)."""
    inventario = Inventario.query.get_or_404(id_inventario)
    data = request.get_json()

    if "stock_actual" in data:
        nuevo_stock = data["stock_actual"]
        producto = Producto.query.get(inventario.id_producto)

        if nuevo_stock < 0:
            return jsonify({"error": "El stock no puede ser negativo"}), 400
        if nuevo_stock > producto.stock_maximo:
            return jsonify({"error": f"El stock máximo permitido es {producto.stock_maximo}"}), 400

        inventario.stock_actual = nuevo_stock
        inventario.fecha_actualizacion = datetime.utcnow()

    db.session.commit()
    return jsonify(inventario.to_dict())


@inventario_bp.post("/<int:id_inventario>/entrada")
def registrar_entrada(id_inventario):
    """Suma unidades al stock actual (ej. llegó mercadería del proveedor)."""
    inventario = Inventario.query.get_or_404(id_inventario)
    data = request.get_json()
    cantidad = data["cantidad"]

    if cantidad <= 0:
        return jsonify({"error": "La cantidad debe ser mayor a cero"}), 400

    producto = Producto.query.get(inventario.id_producto)
    nuevo_stock = inventario.stock_actual + cantidad

    if nuevo_stock > producto.stock_maximo:
        return jsonify({
            "error": f"Esa entrada supera el stock máximo ({producto.stock_maximo}). "
                     f"Actual: {inventario.stock_actual}, intentaste agregar: {cantidad}"
        }), 400

    inventario.stock_actual = nuevo_stock
    inventario.fecha_actualizacion = datetime.utcnow()
    db.session.commit()
    return jsonify(inventario.to_dict())