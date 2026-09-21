from flask import Blueprint, jsonify, request
from models import db, Cliente

cliente_bp = Blueprint("cliente", __name__, url_prefix="/api/clientes")

@cliente_bp.get("")
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@cliente_bp.get("/<int:id_cliente>")
def obtener_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    return jsonify(cliente.to_dict())

@cliente_bp.post("")
def crear_cliente():
    data = request.get_json()
    nuevo = Cliente(
        nombre=data["nombre"],
        telefono=data.get("telefono"),
        correo_electronico=data.get("correo_electronico"),
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201