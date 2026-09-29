from flask import Blueprint, jsonify, request
from models import db, Marca

marca_bp = Blueprint("marca", __name__, url_prefix="/api/marcas")

@marca_bp.get("")
def listar_marcas():
    marcas = Marca.query.all()
    return jsonify([m.to_dict() for m in marcas])

@marca_bp.get("/<int:id_marca>")
def obtener_marca(id_marca):
    marca = Marca.query.get_or_404(id_marca)
    return jsonify(marca.to_dict())

@marca_bp.post("")
def crear_marca():
    data = request.get_json()
    nuevo = Marca(
        nombre=data["nombre"],
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201

@marca_bp.put("/<int:id_marca>")
def actualizar_marca(id_marca):
    marca = Marca.query.get_or_404(id_marca)
    data = request.get_json()
    marca.nombre = data["nombre"]
    db.session.commit()
    return jsonify(marca.to_dict())

@marca_bp.delete("/<int:id_marca>")
def eliminar_marca(id_marca):
    marca = Marca.query.get_or_404(id_marca)
    db.session.delete(marca)
    db.session.commit()
    return jsonify({"message": "Marca eliminada correctamente"}), 200