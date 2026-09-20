from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .marca import Marca
from .categoria import Categoria
from .cliente import Cliente
from .empleado import Empleado
from .proveedor import Proveedor
from .producto import Producto
from .inventario import Inventario
from .venta import Venta
from .detalle_venta import DetalleVenta