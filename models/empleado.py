from . import db

class Empleado(db.Model):
    __tablename__ = "empleados"

    id_empleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {"id_empleado": self.id_empleado, "nombre": self.nombre, "rol": self.rol}