from flask import Blueprint, jsonify, request
from models import db, DetalleVenta, Producto

detalle_venta_bp = Blueprint("detalle_venta", __name__, url_prefix="/api/detalle-ventas")

@detalle_venta_bp.get("")
def listar_detalles():
    detalles = DetalleVenta.query.all()
    return jsonify([d.to_dict() for d in detalles])

@detalle_venta_bp.get("/<int:id_detalle>")
def obtener_detalle(id_detalle):
    detalle = DetalleVenta.query.get_or_404(id_detalle)
    return jsonify(detalle.to_dict())