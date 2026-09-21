from flask import Blueprint, jsonify, request
from models import db, Empleado

empleado_bp = Blueprint("empleado", __name__, url_prefix="/api/empleados")

@empleado_bp.get("")
def listar_empleado():
    empleados = Empleado.query.all()
    return jsonify([e.to_dict() for e in empleados])

@empleado_bp.get("/<int:id_empleado>")
def obtener_empleado(id_empleado):
    empleado = Empleado.query.get_or_404(id_empleado)
    return jsonify(empleado.to_dict())

@empleado_bp.post("")
def crear_empleado():
    data = request.get_json()
    nuevo = Empleado(
        nombre=data["nombre"],
        rol=data["rol"]
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201