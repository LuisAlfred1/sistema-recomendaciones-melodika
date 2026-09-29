from flask import Blueprint, jsonify, request
from models import db, Proveedor

proveedor_bp = Blueprint("proveedor", __name__, url_prefix="/api/proveedores")

@proveedor_bp.get("")
def listar_proveedores():
    proveedores = Proveedor.query.all()
    return jsonify([p.to_dict() for p in proveedores])

@proveedor_bp.get("/<int:id_proveedor>")
def obtener_proveedor(id_proveedor):
    proveedor = Proveedor.query.get_or_404(id_proveedor)
    return jsonify(proveedor.to_dict())

@proveedor_bp.post("")
def crear_proveedor():
    data = request.get_json()
    nuevo = Proveedor(
        id_marca=data.get("id_marca"),
        nombre=data["nombre"],
        telefono=data.get("telefono"),
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201

@proveedor_bp.put("/<int:id_proveedor>")
def actualizar_proveedor(id_proveedor):
    proveedor = Proveedor.query.get_or_404(id_proveedor)
    data = request.get_json()
    proveedor.id_marca = data.get("id_marca", proveedor.id_marca)
    proveedor.nombre = data.get("nombre", proveedor.nombre)
    proveedor.telefono = data.get("telefono", proveedor.telefono)
    db.session.commit()
    return jsonify(proveedor.to_dict())

@proveedor_bp.delete("/<int:id_proveedor>")
def eliminar_proveedor(id_proveedor):
    proveedor = Proveedor.query.get_or_404(id_proveedor)
    db.session.delete(proveedor)
    db.session.commit()
    return jsonify({"message": "Proveedor eliminado correctamente"}), 200