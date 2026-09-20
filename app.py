from flask import Flask
from config import Config
from models import db
from routes.producto import producto_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(producto_bp)

    @app.get("/")
    def home():
        return {"mensaje": "API de Intrumentos Melodika activa"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)