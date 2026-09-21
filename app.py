from flask import Flask
from config import Config
from models import db
from routes.producto import producto_bp
from routes.inventario import inventario_bp
from routes.venta import venta_bp
from routes.detalle_venta import detalle_venta_bp
from routes.empleado import empleado_bp
from routes.cliente import cliente_bp
from routes.proveedor import proveedor_bp
from routes.marca import marca_bp
from routes.categoria import categoria_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(producto_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(venta_bp)
    app.register_blueprint(detalle_venta_bp)
    app.register_blueprint(empleado_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(categoria_bp)

    @app.get("/")
    def home():
        return {"mensaje": "API de Intrumentos Melodika activa"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)