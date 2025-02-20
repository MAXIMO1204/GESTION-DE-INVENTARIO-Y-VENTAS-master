Sistema Gestión de inventario y ventas
Este proyecto consiste en un sistema de gestión para una tienda que permite agregar, editar, eliminar productos
y realizar ventas. Está desarrollado en Python utilizando la librería Tkinter para la interfaz gráfica de usuario
(GUI) y SQLite como base de datos para almacenar la información de los productos y las ventas.

Funcionalidades
1. Gestión de Productos
Agregar Productos: Permite agregar productos a la tienda con su nombre, cantidad y precio.
Editar Productos: Se puede editar los detalles de un producto existente, como su nombre, cantidad y precio.
Eliminar Productos: Permite eliminar productos de la tienda de forma rápida.
Visualizar Productos: Los productos se muestran en una lista detallada con su nombre, cantidad disponible y precio.
2. Gestión de Ventas
Realizar Ventas: Permite realizar ventas de productos, reduciendo la cantidad disponible en la tienda.
Historial de Ventas: Las ventas realizadas se almacenan en la base de datos con la cantidad vendida, el precio y el total de la venta.
Requisitos
Python
Tkinter (para la interfaz gráfica)
SQLite (para la base de datos)

Cómo ejecutar el proyecto

Clonar el repositorio
Instalar dependencias Si aún no tienes Tkinter y SQLite instalados
Interactuar con la aplicación Una vez que la aplicación esté en ejecución, podrás:

Agregar, editar o eliminar productos.
Realizar ventas de productos existentes.
Consultar la lista de productos disponibles en la tienda.
Estructura del Proyecto
main.py               # Archivo principal con el código de la aplicación
tienda.db             # Base de datos SQLite para almacenar productos y ventas
README.md             # Este archivo de documentación
Cómo funciona la base de datos
La base de datos tiene dos tablas principales:

productos: Almacena información de los productos (ID, nombre, cantidad y precio).
ventas: Registra las ventas realizadas (ID de la venta, ID del producto, cantidad vendida, precio y total de la venta).