from . import db

class Marca(db.Model):
    __tablename__ = "marcas"

    id_marca = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id_marca": self.id_marca, "nombre": self.nombre}