from . import db

class Proveedor(db.Model):
    __tablename__ = "proveedores"

    id_proveedor = db.Column(db.Integer, primary_key=True)
    id_marca = db.Column(db.Integer, db.ForeignKey("marcas.id_marca"))
    nombre = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20))

    def to_dict(self):
        return {
            "id_proveedor": self.id_proveedor,
            "id_marca": self.id_marca,
            "nombre": self.nombre,
            "telefono": self.telefono,
        }