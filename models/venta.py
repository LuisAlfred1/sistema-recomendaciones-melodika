from datetime import datetime
from . import db

class Venta(db.Model):
    __tablename__ = "ventas"

    id_venta = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"), nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey("empleados.id_empleado"), nullable=False)
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "id_cliente": self.id_cliente,
            "id_empleado": self.id_empleado,
            "fecha_venta": self.fecha_venta.isoformat() if self.fecha_venta else None,
            "total": float(self.total),
        }