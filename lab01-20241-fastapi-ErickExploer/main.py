from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4, UUID

app = FastAPI()

# Modelo para los productos
class Producto(BaseModel):
    id: Optional[UUID] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None

productos = []


# Función para eliminar un producto
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: UUID):
    for i, p in enumerate(productos):
        if p.id == producto_id:
            del productos[i] 
    raise HTTPException(status_code=204, detail="Producto no encontrado")

# Función para crear un nuevo producto

@app.post("/productos", response_model=Producto)
def crear_producto(producto: Producto):
    producto.id = uuid4()
    productos.append(producto)
    return producto

# Función para listar todos los productos
@app.get("/productos")
def listar_todos_los_productos(stock: Optional[int] = None):
    if stock is not None:
        return [producto for producto in productos if producto.stock == stock]
    else:
        return productos
    
# Función para actualizar un producto completo
@app.put("/productos/{producto_id}", response_model=Producto)
def actualizar_producto_completo(producto_id: UUID, producto_nuevo: Producto):
    for i, p in enumerate(productos):
        if p.id == producto_id:
            productos[i] = producto_nuevo
            return producto_nuevo
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Función para actualizar un producto parcialmente
@app.patch("/productos/{producto_id}", response_model=Producto)
def actualizar_producto_parcialmente(producto_id: UUID, datos_parciales: dict):
    for p in productos:
        if p.id == producto_id:
            for field, value in datos_parciales.items():
                setattr(p, field, value)
            return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Función para listar un producto por su ID
@app.get("/productos/{producto_id}")
def listar_producto_por_id(producto_id: UUID):
    for p in productos:
        if p.id == producto_id:
            return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")
# Función para comprar producto
@app.post("/productos/{producto_id}/comprar", response_model=Producto)
def comprar_producto(producto_id: UUID):
    for producto in productos:
        if producto.id == producto_id:
            producto.stock -= 1
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")
#Funcion para reponer producto
@app.post("/productos/{producto_id}/reponer")
def reponer_stock(producto_id: UUID, cantidad: int):
    # Encuentra el producto con el ID proporcionado
    for producto in productos:
        if producto.id == producto_id:
            producto.stock += cantidad
            return {"mensaje": f"Se han repuesto {cantidad} unidades del producto.", "stock": producto.stock}
    raise HTTPException(status_code=404, detail="Producto no encontrado")




