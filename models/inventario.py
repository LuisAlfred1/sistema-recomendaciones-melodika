from datetime import datetime
from . import db

class Inventario(db.Model):
    __tablename__ = "inventario"

    id_inventario = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id_producto"), nullable=False)
    stock_actual = db.Column(db.Integer, default=0)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id_inventario": self.id_inventario,
            "id_producto": self.id_producto,
            "stock_actual": self.stock_actual,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
        }