import sqlite3
from tkinter import *
from tkinter import messagebox, ttk, Toplevel
from ttkthemes import ThemedTk
from datetime import datetime



# CONEXIÓN A LA BASE DE DATOS
conexion = sqlite3.connect("tienda.db")
cursor = conexion.cursor()

# CREAR TABLAS SI NO EXISTEN
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    cantidad INTEGER,
    precio REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas(
    id INTEGER PRIMARY KEY,
    id_producto INTEGER,
    cantidad INTEGER,
    precio REAL,
    total REAL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_producto) REFERENCES productos (id)
)
''')
conexion.commit()

# FUNCIÓN PARA MOSTRAR LOS PRODUCTOS
def mostrar_productos(busqueda=""):
    # Lógica para mostrar productos en la tabla
    lista_productos.delete(*lista_productos.get_children())
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + busqueda + '%',))
    productos = cursor.fetchall()
    for producto in productos:
        lista_productos.insert("", "end", values=producto)

# FUNCIÓN PARA AGREGAR PRODUCTOS AL CARRITO
carrito = []

def agregar_al_carrito():
    selected_item = lista_productos.selection()
    if selected_item:
        id_producto = lista_productos.item(selected_item[0])["values"][0]
        nombre_producto = lista_productos.item(selected_item[0])["values"][1]
        cantidad_disponible = lista_productos.item(selected_item[0])["values"][2]
        precio = lista_productos.item(selected_item[0])["values"][3]

        cantidad_venta = entry_cantidad_venta.get().strip()

        if cantidad_venta.isdigit():
            cantidad_venta = int(cantidad_venta)
            if 0 < cantidad_venta <= cantidad_disponible:
                subtotal = cantidad_venta * float(precio)
                producto_carrito = {
                    "id": id_producto,
                    "nombre": nombre_producto,
                    "cantidad": cantidad_venta,
                    "precio": precio,
                    "subtotal": subtotal
                }
                carrito.append(producto_carrito)
                actualizar_carrito()
                entry_cantidad_venta.delete(0, END)
            else:
                messagebox.showerror("Error", "Cantidad no válida o insuficiente.")
        else:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")
    else:
        messagebox.showerror("Error", "Seleccione un producto para agregar al carrito.")

# FUNCIÓN PARA ACTUALIZAR EL CARRITO
def actualizar_carrito():
    for item in lista_carrito.get_children():
        lista_carrito.delete(item)

    total_neto = 0
    for producto in carrito:
        lista_carrito.insert("", "end", values=(producto["nombre"], producto["cantidad"], producto["precio"], producto["subtotal"]))
        total_neto += producto["subtotal"]

    label_total_neto.config(text=f"Total Neto: ${total_neto:.2f}")

# FUNCIÓN PARA VACIAR EL CARRITO
def vaciar_carrito():
    respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que desea vaciar el carrito?")
    if respuesta:
        carrito.clear()
        actualizar_carrito()

# FUNCIÓN PARA COMPLETAR LA COMPRA
def completar_compra():
    if carrito:
        for producto in carrito:
            id_producto = producto["id"]
            cantidad_vendida = producto["cantidad"]
            cursor.execute("SELECT cantidad FROM productos WHERE id = ?", (id_producto,))
            cantidad_disponible = cursor.fetchone()[0]
            nueva_cantidad = cantidad_disponible - cantidad_vendida

            if nueva_cantidad < 0:
                messagebox.showerror("Error", f"No hay suficiente stock de {producto['nombre']}.")
                return

            cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_producto))
            cursor.execute('INSERT INTO ventas (id_producto, cantidad, precio, total) VALUES (?, ?, ?, ?)',
                           (id_producto, cantidad_vendida, producto["precio"], producto["subtotal"]))

        conexion.commit()
        carrito.clear()
        actualizar_carrito()
        mostrar_productos()
        messagebox.showinfo("Éxito", "Compra realizada con éxito.")
    else:
        messagebox.showerror("Error", "El carrito está vacío.")

# FUNCIÓN PARA ELIMINAR UN PRODUCTO
def eliminar_producto():
    selected_item = lista_productos.selection()
    if selected_item:
        id_producto = lista_productos.item(selected_item[0])["values"][0]
        respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar este producto?")
        if respuesta:
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conexion.commit()
            mostrar_productos()
            messagebox.showinfo("Éxito", "Producto eliminado con éxito.")
    else:
        messagebox.showerror("Error", "Seleccione un producto para eliminar.")

# FUNCIÓN PARA EDITAR UN PRODUCTO
def editar_producto():
    selected_item = lista_productos.selection()
    if selected_item:
        id_producto = lista_productos.item(selected_item[0])["values"][0]
        nombre_actual = lista_productos.item(selected_item[0])["values"][1]
        cantidad_actual = lista_productos.item(selected_item[0])["values"][2]
        precio_actual = lista_productos.item(selected_item[0])["values"][3]

        top = Toplevel()
        top.title("Editar Producto")

        Label(top, text="Nombre del Producto").pack(pady=5)
        entry_nombre = Entry(top)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack(pady=5)

        Label(top, text="Cantidad").pack(pady=5)
        entry_cantidad = Entry(top)
        entry_cantidad.insert(0, cantidad_actual)
        entry_cantidad.pack(pady=5)

        Label(top, text="Precio").pack(pady=5)
        entry_precio = Entry(top)
        entry_precio.insert(0, precio_actual)
        entry_precio.pack(pady=5)

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get().strip()
            nueva_cantidad = entry_cantidad.get().strip()
            nuevo_precio = entry_precio.get().strip()

            if nuevo_nombre and nueva_cantidad.isdigit() and nuevo_precio.replace('.', '', 1).isdigit():
                cursor.execute('UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?',
                               (nuevo_nombre, int(nueva_cantidad), float(nuevo_precio), id_producto))
                conexion.commit()
                top.destroy()
                mostrar_productos()
            else:
                messagebox.showerror("Error", "Ingrese datos válidos.")

        Button(top, text="Guardar Cambios", command=guardar_cambios).pack(pady=20)

# FUNCIÓN PARA AGREGAR UN NUEVO PRODUCTO
def agregar_producto():
    top = Toplevel()
    top.title("Agregar Producto")

    Label(top, text="Nombre del Producto").pack(pady=5)
    entry_nombre = Entry(top)
    entry_nombre.pack(pady=5)

    Label(top, text="Cantidad").pack(pady=5)
    entry_cantidad = Entry(top)
    entry_cantidad.pack(pady=5)

    Label(top, text="Precio").pack(pady=5)
    entry_precio = Entry(top)
    entry_precio.pack(pady=5)

    def guardar_producto():
        nombre = entry_nombre.get().strip()
        cantidad = entry_cantidad.get().strip()
        precio = entry_precio.get().strip()

        if nombre and cantidad.isdigit() and precio.replace('.', '', 1).isdigit():
            cursor.execute('INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)',
                           (nombre, int(cantidad), float(precio)))
            conexion.commit()
            top.destroy()
            mostrar_productos()
        else:
            messagebox.showerror("Error", "Ingrese datos válidos.")

    Button(top, text="Guardar", command=guardar_producto).pack(pady=20)

# FUNCIÓN PARA MOSTRAR EL TOTAL DE VENTAS DIARIAS
def mostrar_ventas_diarias():
    # Crear una nueva ventana
    ventana_detalle = Toplevel()
    ventana_detalle.title("Detalle de Ventas Diarias")
    
    # Crear un Treeview para mostrar las ventas
    lista_ventas = ttk.Treeview(ventana_detalle, columns=("ID", "Fecha y Hora", "Total"), show="headings")
    lista_ventas.heading("ID", text="ID Venta")
    lista_ventas.heading("Fecha y Hora", text="Fecha y Hora")
    lista_ventas.heading("Total", text="Total")
    lista_ventas.pack(fill="both", expand=True)

    # Consulta para obtener las ventas del día
    cursor.execute("SELECT id, fecha_hora, total FROM ventas ORDER BY fecha_hora ASC")
    ventas = cursor.fetchall()
    
    total_neto = 0.0  # Inicializa el total neto
    for venta in ventas:
        id_venta, fecha_hora, total = venta
        total_neto += total
        
        # Muestra cada venta con su total
        lista_ventas.insert("", "end", values=(id_venta, fecha_hora, total))
    
    # Muestra el total neto al final
    lista_ventas.insert("", "end", values=("Total Neto", "", f"${total_neto:.2f}"), tags=("total",))

    # Ajustar el tamaño de las columnas
    for col in lista_ventas["columns"]:
        lista_ventas.column(col, width=100)
    
    # Iniciar el bucle de la nueva ventana
    ventana_detalle.mainloop()



def calcular_total_neto():
    # Lógica para calcular el total neto
    total_neto = 0.0
    for item in lista_carrito.get_children():
        total_neto += float(lista_carrito.item(item)['values'][3])  # Columna de subtotal
    label_total_neto.config(text=f"Total Neto: ${total_neto:.2f}")

# CREAR LA VENTANA PRINCIPAL
ventana = Tk()
ventana.title("Sistema de Ventas")
ventana.geometry("800x600")

# BARRA DE BOTONES
frame_botones = Frame(ventana)
frame_botones.pack(pady=10)

boton_agregar_producto = Button(frame_botones, text="Agregar Producto", command=agregar_producto)
boton_agregar_producto.pack(side=LEFT, padx=5)

boton_eliminar_producto = Button(frame_botones, text="Eliminar Producto", command=eliminar_producto)
boton_eliminar_producto.pack(side=LEFT, padx=5)

boton_editar_producto = Button(frame_botones, text="Editar Producto", command=editar_producto)
boton_editar_producto.pack(side=LEFT, padx=5)

boton_mostrar_ventas = Button(frame_botones, text="Mostrar Ventas Diarias", command=mostrar_ventas_diarias)
boton_mostrar_ventas.pack(side=LEFT, padx=5)

boton_completar_compra = Button(frame_botones, text="Completar Compra", command=completar_compra)
boton_completar_compra.pack(side=LEFT, padx=5)

boton_vaciar_carrito = Button(frame_botones, text="Vaciar Carrito", command=vaciar_carrito)
boton_vaciar_carrito.pack(side=LEFT, padx=5)

# BARRA DE BÚSQUEDA
label_busqueda = Label(ventana, text="Buscar Producto:")
label_busqueda.pack(pady=10)

entry_busqueda = Entry(ventana, width=30)
entry_busqueda.pack(pady=5)
entry_busqueda.bind("<KeyRelease>", lambda event: mostrar_productos(entry_busqueda.get()))

# TABLA DE PRODUCTOS
lista_productos = ttk.Treeview(ventana, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings")
lista_productos.heading("ID", text="ID Producto")
lista_productos.heading("Nombre", text="Nombre")
lista_productos.heading("Cantidad", text="Cantidad en Stock")
lista_productos.heading("Precio", text="Precio")
lista_productos.pack(pady=10, fill=BOTH, expand=True)

# LABEL Y ENTRY PARA CANTIDAD DE VENTA
label_cantidad_venta = Label(ventana, text="Cantidad:")
label_cantidad_venta.pack(pady=5)

entry_cantidad_venta = Entry(ventana, width=10)
entry_cantidad_venta.pack(pady=5)

# BOTÓN PARA AGREGAR AL CARRITO
boton_agregar = Button(ventana, text="Agregar al Carrito", command=agregar_al_carrito)
boton_agregar.pack(pady=10)

# TABLA DEL CARRITO
lista_carrito = ttk.Treeview(ventana, columns=("Producto", "Cantidad", "Precio", "Subtotal"), show="headings")
lista_carrito.heading("Producto", text="Producto")
lista_carrito.heading("Cantidad", text="Cantidad")
lista_carrito.heading("Precio", text="Precio")
lista_carrito.heading("Subtotal", text="Subtotal")
lista_carrito.pack(pady=10, fill=BOTH, expand=True)


# LABEL PARA MOSTRAR TOTAL NETO
label_total_neto = Label(ventana, text="Total Neto: $0.00", font=("Helvetica", 14))
label_total_neto.pack(pady=10)

# CARGAR PRODUCTOS AL INICIAR
mostrar_productos()

# INICIAR EL BUCLE DE LA VENTANA
ventana.mainloop()

# CERRAR LA CONEXIÓN A LA BASE DE DATOS
conexion.close()