from flask import Blueprint, jsonify, request
from models import db, Inventario

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
        id_producto=data.get("id_producto"),
        stock_actual=data.get("stock_actual", 0),
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201