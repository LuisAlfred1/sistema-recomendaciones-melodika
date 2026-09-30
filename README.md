# Sistema de ventas e inventario - Instrumentos Melodika

![alt text](image.png)

---

## Avances de primera entrega

> [!IMPORTANT]
> Aún no hay interfaz disponible, trabajando solo backend

- Diagrama ER y Caso de Uso
- Conexión con MYSQL
- Modelos creados
- APIs creadas
- Datos iniciales creados: **10 productos - 10 inventarios (1 por producto)**, **2 clientes**, **1 empleado**

---

## Validaciones

### Alerta de stock insuficiente

Con Postman se intento crear una venta añadiendo más productos de lo disponible en stock, **respuesta**:

![alt text](image-1.png)

### Alerta de stock máximo

Se intento actualizar el stock de un producto con una cantidad mayor al stock maximo, **respuesta**:

![alt text](image-3.png)

### Alerta de stock negativo

Se intento actualizar el stock de un producto con una cantidad negativa **respuesta**:

![alt text](image-4.png)

### Creación de venta

Se creó una venta con postman

![alt text](image-2.png)

> [!IMPORTANT]
> **Para dashboard administrativo**:
> Terminar el CRUD para los modelos necesarios y crear/generar las recomendaciones.