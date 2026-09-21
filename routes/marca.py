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