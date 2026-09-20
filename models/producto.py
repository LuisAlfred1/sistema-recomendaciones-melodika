from . import db

class Producto(db.Model):
    __tablename__ = "productos"

    id_producto = db.Column(db.Integer, primary_key=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey("categorias.id_categoria"))
    id_proveedor = db.Column(db.Integer, db.ForeignKey("proveedores.id_proveedor"))
    nombre = db.Column(db.String(150), nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    stock_minimo = db.Column(db.Integer, default=0)
    stock_maximo = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "id_categoria": self.id_categoria,
            "id_proveedor": self.id_proveedor,
            "nombre": self.nombre,
            "precio_unitario": float(self.precio_unitario),
            "stock_minimo": self.stock_minimo,
            "stock_maximo": self.stock_maximo,
        }