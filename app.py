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
    # Creamos una instancia de la aplicación Flask
    app = Flask(__name__)

    # Configuramos la aplicación Flask con los parámetros definidos en la clase Config del archivo config.py
    app.config.from_object(Config)

    # Inicializamos la extensión SQLAlchemy con la aplicación Flask
    db.init_app(app)

    # Registramos los blueprints de las rutas, que permiten organizar las rutas de la aplicación en módulos separados.
    app.register_blueprint(producto_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(venta_bp)
    app.register_blueprint(detalle_venta_bp)
    app.register_blueprint(empleado_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(categoria_bp)

    # Definimos una ruta raíz ("/") que devuelve un mensaje indicando que la API está activa.
    @app.get("/")
    def home():
        return {"mensaje": "API de Intrumentos Melodika activa"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)