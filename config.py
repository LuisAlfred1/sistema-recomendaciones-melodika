import os
from dotenv import load_dotenv

load_dotenv()

# La clase Config se utiliza para almacenar la configuración de la aplicación Flask, incluyendo la URI de la base de datos y otras configuraciones relacionadas con SQLAlchemy.
class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    # Usamos SQLAlchemy para conectarnos a la base de datos MySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    # Desactivamos el seguimiento de modificaciones para mejorar el rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False