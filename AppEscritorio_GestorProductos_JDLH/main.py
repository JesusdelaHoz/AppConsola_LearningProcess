from tkinter import ttk
from tkinter import *
import sqlite3

class Producto:

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1)
        self.ventana.wm_iconbitmap("recursos/M6_P2_icon.ico")

        # Creacion del contenedor Frame principal
        frame = LabelFrame(self.ventana, text = "Registro de nuevo produto", )
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text = "Nombre: ")
        self.etiqueta_nombre.grid(row=1, column=0)
        # Entry Nombre
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1, columnspan=2 ,sticky= W + E)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1, columnspan=2, sticky= W + E)

        # Label Calidad
        self.etiqueta_calidad = Label(frame, text="Calidad: ")
        self.etiqueta_calidad.grid(row=3, column=0,)
        # Entry Calidad
        self.calidad = Entry(frame)
        self.calidad.grid(row=3, column=1, columnspan=2, sticky= W + E)

        # Boton de Añadir Producto
        self.boton_aniadir = ttk.Button(frame, text = "Guardar Producto", command= self.add_producto) # NO METER LOS
        self.boton_aniadir.grid(row=4, columnspan=3, sticky= W + E)                                   # PARENTESIS

        # Label de Validacion
        self.mensaje = Label(text="", fg= "red")
        self.mensaje.grid(row=5, column = 0, columnspan=3, sticky= W + E)

        # Tabla Productos
        # Estilo personalizado para la tabla creado por nosotros
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(frame, height=20, columns=[f"{n}" for n in range(0, 2)], style= "mystyle.Treeview")
        self.tabla.grid(row=5, column=0, columnspan=3)
        self.tabla.heading("#0", text="Nombre", anchor=CENTER)
        self.tabla.heading("#1", text="Precio", anchor=CENTER)
        self.tabla.heading("#2", text="Calidad", anchor=CENTER)

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))

        boton_eliminar = ttk.Button(text='ELIMINAR', style='my.TButton', command= self.del_productos)
        boton_eliminar.grid(row= 6, column=0, columnspan=1, sticky=W + E)
        boton_editar = ttk.Button(text='EDITAR', style='my.TButton', command= self.edit_producto)
        boton_editar.grid(row= 6, column=1, columnspan=1, sticky=W + E)

        self.get_productos()

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):

        registros_tabla =  self.tabla.get_children()
        for i in registros_tabla:
            self.tabla.delete(i)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)
        for i in registros:
            print(i)
            self.tabla.insert("", 0, text= i[1], values= (i[2], i[3]))

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_calidad(self):
        calidad_introducido_por_usuario = self.calidad.get()
        return len(calidad_introducido_por_usuario) != 0 \
               and calidad_introducido_por_usuario == "Buena" \
               or calidad_introducido_por_usuario == "Media" \
               or calidad_introducido_por_usuario =="Baja"

    def add_producto(self):
        if self.validacion_calidad() and self.validacion_precio() and self.validacion_nombre():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get(), self.calidad.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            # Para Debug
            # print(self.nombre.get())
            # print(self.precio.get())
            # print(self.calidad.get())

        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_calidad() == False:
            print("La calidad debe ser 'Buena, Media o Baja' y es obligatoria")
            self.mensaje["text"] = "La calidad debe ser 'Buena, Media o Baja' y es obligatoria"
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_calidad():
            print("El precio es obligatorio")
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre()== False and self.validacion_precio() and self.validacion_calidad():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es obligatorio"
        else:
            print("Todos los campos son obligatorios")
            self.mensaje["text"] = "Todos los campos son obligatorios"

        self.get_productos()  # Actualizacion de producto

    def del_productos(self):
        nombre =self.tabla.item(self.tabla.selection())['text']
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.get_productos()

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]  # El precio se encuentra dentro de una lista
        calidad_vieja = self.tabla.item(self.tabla.selection())['values'][1]

        # Ventana nueva (editar producto)
        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana
        self.ventana_editar.resizable(1, 1)
        self.ventana_editar.wm_iconbitmap('recursos/M6_P2_icon.ico')  # Icono de la ventana
        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto")  #frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_anituguo.grid(row=2, column=0)  # Posicionamiento a traves de grid
        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly')
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ")
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_antiguo.grid(row=4, column=0)  # Posicionamiento a traves de grid
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep,textvariable=StringVar(self.ventana_editar, value=old_precio),state='readonly')
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ")
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Calidad antigua
        self.etiqueta_calidad_antiguo = Label(frame_ep, text="Precio antiguo: ")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_calidad_antiguo.grid(row=6, column=0)  # Posicionamiento a traves de grid
        # Entry Calidad antigua (texto que no se podra modificar)
        self.input_calidad_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=calidad_vieja), state='readonly')
        self.input_calidad_antiguo.grid(row=6, column=1)

        # Label Calidad nueva
        self.etiqueta_calidad_nuevo = Label(frame_ep, text="Calidad nueva: ")
        self.etiqueta_calidad_nuevo.grid(row=7, column=0)
        # Entry Calidad nueva (texto que si se podra modificar)
        self.input_calidad_nuevo = Entry(frame_ep)
        self.input_calidad_nuevo.grid(row=7, column=1)

        # Boton Actualizar Producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",
                                           command=lambda:
        self.actualizar_productos(self.input_nombre_nuevo.get(),
        self.input_nombre_antiguo.get(),
        self.input_precio_nuevo.get(),
        self.input_precio_antiguo.get(),
        self.input_calidad_nuevo.get(),
        self.input_calidad_antiguo.get()))

        self.boton_actualizar.grid(row=8, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_calidad, antigua_calidad):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, calidad = ? WHERE nombre = ? AND precio = ? AND calidad = ?'
        if nuevo_nombre != '' and nuevo_precio != '' and nueva_calidad != '':
            # Si el usuario escribe nuevo nombre, nuevo precio y nueva calidad, se cambian todos
            parametros = (nuevo_nombre, nuevo_precio, nueva_calidad, antiguo_nombre, antiguo_precio, antigua_calidad)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_calidad != '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (nuevo_nombre, antiguo_precio, nueva_calidad, antiguo_nombre, antiguo_precio, antigua_calidad)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_calidad != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, nueva_calidad, antiguo_nombre, antiguo_precio, antigua_calidad)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_calidad == '':
            # Si el usuario deja vacio la neuva calidad, se mantiene la calidad anterior
            parametros = (nuevo_nombre, nuevo_precio, antigua_calidad, antiguo_nombre, antiguo_precio, antigua_calidad)
            producto_modificado = True

        if (producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre) # Mostrar mensaje para el usuario

if __name__ == '__main__':
    root = Tk()
    app = Producto(root)
    root.mainloop()