from flask import Blueprint, jsonify, request
from models import db, Categoria

categoria_bp = Blueprint("categoria", __name__, url_prefix="/api/categorias")

@categoria_bp.get("")
def listar_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.to_dict() for c in categorias])

@categoria_bp.get("/<int:id_categoria>")
def obtener_categoria(id_categoria):
    categoria = Categoria.query.get_or_404(id_categoria)
    return jsonify(categoria.to_dict())

@categoria_bp.post("")
def crear_categoria():
    data = request.get_json()
    nuevo = Categoria(
        nombre=data["nombre"],
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201

@categoria_bp.put("/<int:id_categoria>")
def actualizar_categoria(id_categoria):
    categoria = Categoria.query.get_or_404(id_categoria)
    data = request.get_json()
    categoria.nombre = data["nombre"]
    db.session.commit()
    return jsonify(categoria.to_dict())

@categoria_bp.delete("/<int:id_categoria>")
def eliminar_categoria(id_categoria):
    categoria = Categoria.query.get_or_404(id_categoria)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"message": "Categoría eliminada correctamente"}), 200