from sqlalchemy import create_engine, text
from config import Config

print("URI generada:", Config.SQLALCHEMY_DATABASE_URI)

try:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        resultado = conn.execute(text("SHOW TABLES"))
        tablas = [fila[0] for fila in resultado]
        print("Conexión exitosa. Tablas encontradas:")
        for t in tablas:
            print("  -", t)
except Exception as e:
    print("Falló la conexión:")
    print(e)