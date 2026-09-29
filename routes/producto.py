from flask import Blueprint, jsonify, request
from models import db, Producto

producto_bp = Blueprint("producto", __name__, url_prefix="/api/productos")

@producto_bp.get("")
def listar_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos])

@producto_bp.get("/<int:id_producto>")
def obtener_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    return jsonify(producto.to_dict())

@producto_bp.post("")
def crear_producto():
    data = request.get_json()
    nuevo = Producto(
        id_categoria=data.get("id_categoria"),
        id_proveedor=data.get("id_proveedor"),
        nombre=data["nombre"],
        precio_unitario=data["precio_unitario"],
        stock_minimo=data.get("stock_minimo", 0),
        stock_maximo=data.get("stock_maximo", 0),
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201

@producto_bp.put("/<int:id_producto>")
def actualizar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    data = request.get_json()
    producto.id_categoria = data.get("id_categoria", producto.id_categoria)
    producto.id_proveedor = data.get("id_proveedor", producto.id_proveedor)
    producto.nombre = data.get("nombre", producto.nombre)
    producto.precio_unitario = data.get("precio_unitario", producto.precio_unitario)
    producto.stock_minimo = data.get("stock_minimo", producto.stock_minimo)
    producto.stock_maximo = data.get("stock_maximo", producto.stock_maximo)
    db.session.commit()
    return jsonify(producto.to_dict())

@producto_bp.delete("/<int:id_producto>")
def eliminar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"message": "Producto eliminado correctamente"}), 200