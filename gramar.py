import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

import sys
import traceback

import tkinter as tk
import traceback



def main():
    try:
        root = tk.Tk()
        app = GestionClientes(root)
        root.mainloop()
    except Exception:
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())

import sys
import os

def obtener_ruta_recurso(relative_path):
    """Obtiene la ruta absoluta del recurso, compatible con PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from PIL import Image, ImageTk

image_path = obtener_ruta_recurso("icons/logoGramar.png")
image = Image.open(image_path)

            
# # Función para obtener la ruta correcta en el ejecutable
# def resource_path(relative_path):
#     """ Devuelve la ruta de un archivo dentro del paquete ejecutable """
#     try:
#         # Para PyInstaller, cuando el programa está empaquetado
#         base_path = sys._MEIPASS
#     except Exception:
#         # Si no está empaquetado, devuelve la ruta relativa
#         base_path = os.path.abspath(".")
    
#     return os.path.join(base_path, relative_path)

def aplicar_estilo():
    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure("Treeview", font=('Segoe UI', 10), rowheight=25)
    estilo.configure("TButton", font=('Segoe UI', 10), padding=5)
    estilo.configure("TLabel", font=('Segoe UI', 10))


def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

class GestionClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Clientes")
        self.conectar_db()
        self.crear_gui()
    
    def aplicar_estilo():
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure("Treeview", font=('Segoe UI', 10), rowheight=25)
        estilo.configure("TButton", font=('Roboto', 10), padding=5)
        estilo.configure("TLabel", font=('Segoe UI', 10))
        


    def centrar_ventana(ventana, ancho, alto):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_gui(self):
         # Contenedor para imagen y título
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10)

        # Cargar imagen

        # Cambiar la ruta al usar la función resource_path
        #image_path = resource_path("icons/logoGramar.png")
        image = Image.open(image_path)

        image = image.resize((120, 120), Image.Resampling.LANCZOS)


        image = image.resize((300, 100), Image.Resampling.LANCZOS)
                                                                      # Ajustá el tamaño si querés
        self.logo_img = ImageTk.PhotoImage(image)  # Guardamos como atributo para que no se borre por el recolector

        logo_label = tk.Label(header_frame, image=self.logo_img)
        logo_label.pack()

        # Título debajo de la imagen
        titulo = ttk.Label(header_frame, text="Gestion de clientes", font=("Roboto", 30, "bold"))
        titulo.pack(pady=5)
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding=20)
        frame_principal.pack(fill="both", expand=True)

        # Frame para búsqueda
        frame_busqueda = ttk.Frame(frame_principal)
        frame_busqueda.pack(pady=10)

        ttk.Label(frame_busqueda, text="Buscar cliente:", font=("Roboto", 16)).pack(side="left", padx=5)
        self.entry_busqueda = ttk.Entry(frame_busqueda, font=("Roboto", 16), width=40)
        self.entry_busqueda.pack(side="left", padx=5)
        ttk.Button(frame_busqueda, text="Buscar", width=20, command=self.buscar_cliente).pack(side="left")

        # Frame para tabla
        frame_tabla = ttk.Frame(frame_principal)
        frame_tabla.pack(pady=20)

        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Nombre", "Dirección", "Teléfono", "Horario"),
            show="headings",
            height=10
        )

        for col in ("ID", "Nombre", "Dirección", "Teléfono", "Horario"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack()

        # self.tree.bind("<Double-1>", self.abrir_fotocopiadoras)
        self.tree.bind("<Return>", self.abrir_fotocopiadoras)

        # Frame para botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=15)

        ttk.Button(frame_botones, text="Agregar Cliente", command=self.agregar_cliente).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Editar Cliente", command=self.editar_cliente).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Eliminar Cliente", command=self.eliminar_cliente).pack(side="left", padx=10)

        self.mostrar_clientes()




    def conectar_db(self):
        self.conn = sqlite3.connect("gramar.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                horario TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fotocopiadoras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                ubicacion TEXT NOT NULL,
                modelo TEXT NOT NULL,
                voltaje TEXT NOT NULL,
                contador_copias INTEGER,
                numero_serie TEXT NOT NULL UNIQUE,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fotocopiadora_id INTEGER NOT NULL,
                cambio_toner TEXT,
                cambio_ui TEXT,
                cambio_fusor TEXT,
                contador INTEGER,
                observaciones TEXT,
                servicio_realizado TEXT,
                fecha_servicio TEXT,
                FOREIGN KEY (fotocopiadora_id) REFERENCES fotocopiadoras(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()


    def mostrar_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM clientes")
        for cliente in self.cursor.fetchall():
            self.tree.insert("", "end", values=cliente)
        
        
        # Seleccionar primer ítem
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])  # marca el primero
            self.tree.focus(items[0])          # le da el foco
            self.tree.focus_set() 

    
    def buscar_cliente(self):
        nombre_buscar = self.entry_busqueda.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM clientes WHERE nombre LIKE ?", (f"%{nombre_buscar}%",))
        for cliente in self.cursor.fetchall():
            self.tree.insert("", "end", values=cliente)
        # Seleccionar primer ítem
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])  # marca el primero
            self.tree.focus(items[0])          # le da el foco
            self.tree.focus_set() 

    def agregar_cliente(self):
        self.abrir_formulario_cliente()
    
    def editar_cliente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para editar")
            return
        datos = self.tree.item(seleccionado[0], "values")
        self.abrir_formulario_cliente(datos)
    
    def eliminar_cliente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
            return
        cliente_id = self.tree.item(seleccionado[0], "values")[0]
        self.cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        self.conn.commit()
        self.mostrar_clientes()
    
    def abrir_formulario_cliente(self, datos=None):
        form = tk.Toplevel(self.root)
        form.title("Formulario Cliente")
        
        ttk.Label(form, text="Nombre:").grid(row=0, column=0)
        nombre = ttk.Entry(form)
        nombre.grid(row=0, column=1)
        
        ttk.Label(form, text="Dirección:").grid(row=1, column=0)
        direccion = ttk.Entry(form)
        direccion.grid(row=1, column=1)
        
        ttk.Label(form, text="Teléfono:").grid(row=2, column=0)
        telefono = ttk.Entry(form)
        telefono.grid(row=2, column=1)
        
        ttk.Label(form, text="Horario:").grid(row=3, column=0)
        horario = ttk.Entry(form)
        horario.grid(row=3, column=1)
        
        if datos:
            nombre.insert(0, datos[1])
            direccion.insert(0, datos[2])
            telefono.insert(0, datos[3])
            horario.insert(0, datos[4])
        
        ttk.Button(form, text="Guardar", command=lambda: self.guardar_cliente(datos[0] if datos else None, nombre.get(), direccion.get(), telefono.get(), horario.get(), form)).grid(row=4, columnspan=2)
    
    def guardar_cliente(self, cliente_id, nombre, direccion, telefono, horario, form):
        if cliente_id:
            self.cursor.execute("UPDATE clientes SET nombre=?, direccion=?, telefono=?, horario=? WHERE id=?", (nombre, direccion, telefono, horario, cliente_id))
        else:
            self.cursor.execute("INSERT INTO clientes (nombre, direccion, telefono, horario) VALUES (?, ?, ?, ?)", (nombre, direccion, telefono, horario))
        self.conn.commit()
        form.destroy()
        self.mostrar_clientes()

    def abrir_fotocopiadoras(self, event):
        seleccionado = self.tree.selection()
        if not seleccionado:
            return
        cliente_id = self.tree.item(seleccionado[0], "values")[0]
        self.ventana_fotocopiadoras(cliente_id)
    
    def ventana_fotocopiadoras(self, cliente_id):
        ventana = tk.Toplevel(self.root)
        ventana.title("Fotocopiadoras del Cliente")

        # Posicionar en el mismo lugar que la ventana principal
        self.root.update_idletasks()
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        ventana.geometry(f"+{x}+{y}")

        
    
        ventana.geometry("+{}+{}".format(self.root.winfo_x(), self.root.winfo_y()))

        tree = ttk.Treeview(ventana, columns=("ID", "Cliente_id", "Ubicacion", "Modelo", "Voltaje", "Contador Copias", "N° Serie"), show="headings")
        for col in ("ID", "Cliente_id", "Ubicacion", "Modelo", "Voltaje", "Contador Copias", "N° Serie"):
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(pady=10)

        

        tree.bind("<Double-1>", lambda event: self.abrir_servicios(tree))
        tree.bind("<Return>", lambda event: self.abrir_servicios(tree))
        


        btn_frame = ttk.Frame(ventana)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Agregar Fotocopiadora", command=lambda: self.abrir_formulario_fotocopiadora(cliente_id, tree)).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Editar Fotocopiadora", command=lambda: self.editar_fotocopiadora(tree)).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar Fotocopiadora", command=lambda: self.eliminar_fotocopiadora(tree)).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Ver Servicios", command=lambda: self.abrir_servicios(tree)).grid(row=0, column=3, padx=5)

        self.mostrar_fotocopiadoras(cliente_id, tree)



    def mostrar_fotocopiadoras(self, cliente_id, tree):
        """Mostrar las fotocopiadoras de un cliente"""
        for row in tree.get_children():
            tree.delete(row)
        self.cursor.execute("SELECT * FROM fotocopiadoras WHERE cliente_id=?", (cliente_id,))
        for fotocopiadora in self.cursor.fetchall():
            tree.insert("", "end", values=fotocopiadora)

        # Seleccionar primer ítem
        items = tree.get_children()
        if items:
            tree.selection_set(items[0])  # marca el primero
            tree.focus(items[0])          # le da el foco
            tree.focus_set() 

    def abrir_formulario_fotocopiadora(self, cliente_id, tree, datos=None):
        """Formulario para agregar o editar fotocopiadora"""
        form = tk.Toplevel(self.root)
        form.title("Formulario Fotocopiadora")

        ttk.Label(form, text="Ubicacion:").grid(row=0, column=0)
        marca = ttk.Entry(form)
        marca.grid(row=0, column=1)

        ttk.Label(form, text="Modelo:").grid(row=1, column=0)
        modelo = ttk.Entry(form)
        modelo.grid(row=1, column=1)

        ttk.Label(form, text="Voltaje:").grid(row=2, column=0)
        voltaje = ttk.Entry(form)
        voltaje.grid(row=2, column=1)

        ttk.Label(form, text="Contador de Copias:").grid(row=3, column=0)
        contador_copias = ttk.Entry(form)
        contador_copias.grid(row=3, column=1)

        ttk.Label(form, text="Número de Serie:").grid(row=4, column=0)
        numero_serie = ttk.Entry(form)
        numero_serie.grid(row=4, column=1)

        if datos:
            marca.insert(0, datos[2])
            modelo.insert(0, datos[3])
            voltaje.insert(0, datos[4])
            contador_copias.insert(0, datos[5])
            numero_serie.insert(0, datos[6])

        ttk.Button(form, text="Guardar", command=lambda: self.guardar_fotocopiadora(cliente_id, marca.get(), modelo.get(), voltaje.get(), contador_copias.get(), numero_serie.get(), form, tree, datos[0] if datos else None)).grid(row=5, columnspan=2)

    def guardar_fotocopiadora(self, cliente_id, marca, modelo, voltaje, contador_copias, numero_serie, form, tree, id_fotocopiadora=None):
        """Guardar fotocopiadora"""
        if id_fotocopiadora:
            self.cursor.execute("UPDATE fotocopiadoras SET marca=?, modelo=?, voltaje=?, contador_copias=?, numero_serie=? WHERE id=?", (marca, modelo, voltaje, contador_copias, numero_serie, id_fotocopiadora))
        else:
            self.cursor.execute("INSERT INTO fotocopiadoras (cliente_id, ubicacion, modelo, voltaje, contador_copias, numero_serie) VALUES (?, ?, ?, ?, ?, ?)", (cliente_id, marca, modelo, voltaje, contador_copias, numero_serie))
        self.conn.commit()
        form.destroy()
        self.mostrar_fotocopiadoras(cliente_id, tree)

    def editar_fotocopiadora(self, tree):
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una fotocopiadora para editar")
            return
        datos = tree.item(seleccionado[0], "values")
        self.abrir_formulario_fotocopiadora(datos[1], tree, datos)  # cliente_id, tree, datos

    def eliminar_fotocopiadora(self, tree):
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una fotocopiadora para eliminar")
            return
        fotocopiadora_id = tree.item(seleccionado[0], "values")[0]
        self.cursor.execute("DELETE FROM fotocopiadoras WHERE id=?", (fotocopiadora_id,))
        self.conn.commit()
        self.mostrar_fotocopiadoras(tree.item(seleccionado[0], "values")[1], tree)  # cliente_id

            
    def abrir_servicios(self, tree):
        seleccionado = tree.selection()
        if not seleccionado:
            return
        fotocopiadora_id = tree.item(seleccionado[0], "values")[0]
        self.ventana_servicios(fotocopiadora_id)
    
    def ventana_servicios(self, fotocopiadora_id):
        ventana = tk.Toplevel(self.root)
        ventana.title("Servicios Realizados")

        # 🪄 Posicionarse sobre la ventana de fotocopiadoras
        self.root.update_idletasks()
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        ventana.geometry(f"+{x}+{y}")

        tree = ttk.Treeview(
            ventana,
            columns=("ID",'Equipo ID' ,"Cambio Tóner", "Cambio UI", "Cambio Fusor", "Último Contador", "Observaciones", "Servicio Realizado", 'Fecha'),
            show="headings"
        )
        

        columnas = {
            "ID": 50,
            'Equipo ID':50,
            "Cambio Tóner": 100,
            "Cambio UI": 100,
            "Cambio Fusor": 100,
            "Último Contador": 100,
            "Observaciones": 200,
            "Servicio Realizado": 250,
            'Fecha': 150
        }

        for col, ancho in columnas.items():
            tree.heading(col, text=col)
            tree.column(col, width=ancho, anchor="center")

        tree.pack(pady=10)

        # 🧩 Botones debajo de la tabla
        btns_frame = ttk.Frame(ventana)
        btns_frame.pack(pady=10)

        ttk.Button(btns_frame, text="Agregar Pedido de Servicio", command=lambda: self.abrir_pedido_servicio(fotocopiadora_id)).pack(side="left", padx=5)
        ttk.Button(btns_frame, text="Agregar Servicio Realizado", command=lambda: self.abrir_formulario_servicio_realizado(fotocopiadora_id, tree)).pack(side="left", padx=5)
        botones_frame = ttk.Frame(ventana)
        botones_frame.pack(pady=10)

        ttk.Button(botones_frame, text="Editar Servicio", command=lambda: self.editar_servicio(tree)).grid(row=0, column=0, padx=5)
        ttk.Button(botones_frame, text="Eliminar Servicio", command=lambda: self.eliminar_servicio(tree)).grid(row=0, column=1, padx=5)

        self.mostrar_servicios(fotocopiadora_id, tree)


    
    def mostrar_servicios(self, fotocopiadora_id, tree):
        for row in tree.get_children():
            tree.delete(row)
        self.cursor.execute("SELECT * FROM servicios WHERE fotocopiadora_id=? ORDER BY fecha_servicio DESC", (fotocopiadora_id,))
        for servicio in self.cursor.fetchall():
            tree.insert("", 0, values=servicio)

        # Seleccionar primer ítem
        items = tree.get_children()
        if items:
            tree.selection_set(items[0])  # marca el primero
            tree.focus(items[0])          # le da el foco
            tree.focus_set() 
    
    def abrir_pedido_servicio(self, fotocopiadora_id):
        form = tk.Toplevel(self.root)
        form.title("Pedido de Servicio")
        
        ttk.Label(form, text="Problema Manifestado:").grid(row=0, column=0)
        problema = ttk.Entry(form)
        problema.grid(row=0, column=1)
        
        ttk.Button(form, text="Generar Pedido", command=lambda: self.generar_pedido(fotocopiadora_id, problema.get(), form)).grid(row=1, columnspan=2)
    
    def generar_pedido(self, fotocopiadora_id, problema, form):
        # Traer datos del cliente y fotocopiadora
        self.cursor.execute("""
            SELECT c.nombre, c.direccion, f.ubicacion, f.modelo, f.voltaje
            FROM clientes c
            JOIN fotocopiadoras f ON c.id = f.cliente_id
            WHERE f.id=?
        """, (fotocopiadora_id,))
        
        datos = self.cursor.fetchone()

        # Traer los últimos 3 servicios
        self.cursor.execute("""
            SELECT servicio_realizado, fecha_servicio, observaciones
            FROM servicios
            WHERE fotocopiadora_id=?
            ORDER BY id DESC
            LIMIT 3
        """, (fotocopiadora_id,))
        ultimos_servicios = self.cursor.fetchall()

        # ultima_observacion = ultimos_servicios[0][2] if ultimos_servicios else ""
        if ultimos_servicios:
            ultima_fecha = ultimos_servicios[0][1]
            ultima_observacion = f"{ultimos_servicios[0][2]} (Fecha: {ultima_fecha})"
        else:
            ultima_observacion = ""

        if datos:
            self.generar_pedido_pdf(datos, problema, ultimos_servicios, ultima_observacion)
        
        form.destroy()


    def generar_pedido_pdf(self, datos_cliente, problema, ultimos_servicios, ultima_observacion):
        nombre_archivo = "pedido_servicio.pdf"
        ruta_logo = "icons/logoGramar.png"
        c = canvas.Canvas(nombre_archivo, pagesize=A4)
        width, height = A4

        # Logo
        if os.path.exists(ruta_logo):
            c.drawImage(ruta_logo, 200, height - 150, width=200, height=150, preserveAspectRatio=True)

        # Título
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 5*cm, "Pedido de Servicio - Abonos")

        # Datos cliente
        x = 4 * cm
        y = height - 8 * cm
        c.setFont("Helvetica", 16)
        campos = ["Cliente", "Dirección", "Ubicacion", "Modelo", "Problema Manifestado"]
        valores = list(datos_cliente)
        valores[3] = f"{valores[3]} ({valores[4]})"
        valores.pop(4)

        for i, valor in enumerate(valores + [problema]):
            c.drawString(x, y - i*1.2*cm, f"{campos[i]}: {valor}")

        # Fecha
        c.drawString(x, y - 7.5*cm, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

        # Últimos servicios
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y - 9*cm, "Últimos Servicios:")

        c.setFont("Helvetica", 11)
        if ultimos_servicios:
            for idx, (servicio, fecha, _) in enumerate(ultimos_servicios):
                c.drawString(x + 1*cm, y - (9.8 + idx*0.7)*cm, f"- {fecha}: {servicio}")
        else:
            c.drawString(x + 1*cm, y - 9.8*cm, "No hay servicios registrados.")

        # Última observación
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y - 12*cm, "Última Observación:")

        c.setFont("Helvetica", 11)
        if ultima_observacion:
            c.drawString(x + 1*cm, y - 12.8*cm, ultima_observacion)
        else:
            c.drawString(x + 1*cm, y - 12.8*cm, "Sin observaciones registradas.")

        # Obsesrvaciones
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y - 13.5*cm, "Observaciones:")
        c.setFont("Helvetica", 12)
        # for i in range(3):  # 5 líneas
        #     c.line(x, y - (9.5 + i * 0.7) * cm, width - x, y - (9.5 + i * 0.7) * cm)

        # Trabajo realizado
        c.setFont('Helvetica-Bold', 12)
        c.drawString(x, y - 16.5*cm, 'Trabajo realizado:' )
        c.setFont('Helvetica', 12)
        

        # Firma
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, 2*cm, "Firma del Cliente:")
        c.line(x + 4*cm, 2*cm, x + 12*cm, 2*cm)

        c.save()

        os.system(f"open {nombre_archivo}")

    # def generar_pedido_pdf(self, datos_cliente, problema):
    #     nombre_archivo = "pedido_servicio.pdf"
    #     # Ruta relativa directa
    #     ruta_logo = "icons/logoGramar.png"
    #     c = canvas.Canvas(nombre_archivo, pagesize=A4)
    #     width, height = A4

    #     if os.path.exists(ruta_logo):
    #         c.drawImage(ruta_logo, 200, height - 150, width=200, height=150, preserveAspectRatio=True)

    #     # Título
    #     c.setFont("Helvetica-Bold", 16)
    #     c.drawCentredString(width / 2, height - 5*cm, "Pedido de Servicio - Abonos")

    #     # Datos del cliente y la fotocopiadora
    #     x = 4 * cm
    #     y = height - 8 * cm
    #     c.setFont("Helvetica", 16)
    #     campos = ["Cliente", "Dirección", "Ubicacion", "Modelo", "Problema Manifestado"]
    #     valores = list(datos_cliente)
    #     # Insertamos el voltaje en el modelo, y eliminamos el voltaje como campo separado
    #     valores[3] = f"{valores[3]} ({valores[4]})"  # Modelo + (Voltaje)
    #     valores.pop(4)  # Quitamos el voltaje ya que está incluido en el modelo

    #     for i, valor in enumerate(valores + [problema]):
    #         c.drawString(x, y - i*1.2*cm, f"{campos[i]}: {valor}")

    #     # Fecha
    #     c.drawString(x, y - 7.5*cm, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

    #     # Espacios para observaciones y trabajo realizado
    #     # Observaciones
    #     c.setFont("Helvetica-Bold", 12)
    #     c.drawString(x, y - 9*cm, "Observaciones:")
    #     #c.setFont("Helvetica", 12)
    #     #for i in range(5):  # 5 líneas
    #         #c.line(x, y - (9.5 + i * 0.7) * cm, width - x, y - (9.5 + i * 0.7) * cm)

    #     # Trabajo Realizado
    #     c.setFont("Helvetica-Bold", 12)
    #     c.drawString(x, y - 13.5*cm, "Trabajo Realizado:")
    #     #c.setFont("Helvetica", 12)
    #     #for i in range(5):  # 5 líneas
    #         #c.line(x, y - (14 + i * 0.7) * cm, width - x, y - (14 + i * 0.7) * cm)

    #     # Firma del cliente
    #     c.setFont("Helvetica-Bold", 12)
    #     c.drawString(x, 2*cm, "Firma del Cliente:")
    #     c.line(x + 4*cm, 2*cm, x + 12*cm, 2*cm)


    #     c.save()

    #     # Abrir automáticamente el PDF (compatible con macOS)
    #     os.system(f"open {nombre_archivo}")

    # def generar_pedido(self, fotocopiadora_id, problema, form):
    #     self.cursor.execute("""
    #         SELECT c.nombre, c.direccion, f.ubicacion, f.modelo, f.voltaje
    #         FROM clientes c
    #         JOIN fotocopiadoras f ON c.id = f.cliente_id
    #         WHERE f.id=?
    #     """, (fotocopiadora_id,))
        
    #     datos = self.cursor.fetchone()
        
    #     if datos:
    #         self.generar_pedido_pdf(datos, problema)
    #         # messagebox.showinfo("Pedido de Servicio", "Pedido en PDF generado correctamente.")
        
    #     form.destroy()

    
    def abrir_formulario_servicio_realizado(self, fotocopiadora_id, tree):
        form = tk.Toplevel(self.root)
        form.title("Servicio Realizado")

        campos = ["Cambio Tóner", "Cambio UI", "Cambio Fusor", "Último Contador", "Observaciones", "Servicio Realizado"]
        entradas = {}

        for i, campo in enumerate(campos):
            ttk.Label(form, text=campo + ":").grid(row=i, column=0)
            entrada = ttk.Entry(form)
            entrada.grid(row=i, column=1)
            entradas[campo] = entrada

        ttk.Button(form, text="Guardar", command=lambda: self.guardar_servicio_realizado(fotocopiadora_id, entradas, form, tree)).grid(row=len(campos), columnspan=2)

    def guardar_servicio_realizado(self, fotocopiadora_id, entradas, form, tree):
        datos = [entrada.get() for entrada in entradas.values()]
        
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        
        # Insertar el nuevo servicio
        self.cursor.execute("""
            INSERT INTO servicios (
                fotocopiadora_id, cambio_toner, cambio_ui, cambio_fusor,
                contador, observaciones, servicio_realizado, fecha_servicio
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (fotocopiadora_id, *datos, fecha_actual))
        
        # Extraer el valor del contador del servicio
        contador = datos[3]  # índice 3 porque el orden de tus entradas es:
                            # cambio_toner, cambio_ui, cambio_fusor, contador, observaciones, servicio_realizado
                            # entonces contador es el 4° elemento (índice 3)
        
        # Actualizar el contador en la tabla fotocopiadoras
        self.cursor.execute("""
            UPDATE fotocopiadoras SET contador_copias = ? WHERE id = ?
        """, (contador, fotocopiadora_id))


        self.conn.commit()
        form.destroy()
        self.mostrar_servicios(fotocopiadora_id, tree)

    def eliminar_servicio(self, tree):
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccioná un servicio para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que querés eliminar este servicio?")
        if confirmacion:
            servicio_id = tree.item(seleccionado[0], "values")[0]
            self.cursor.execute("DELETE FROM servicios WHERE id=?", (servicio_id,))
            self.conn.commit()
            tree.delete(seleccionado[0])
            messagebox.showinfo("Eliminado", "Servicio eliminado correctamente.")

    def editar_servicio(self, tree):
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccioná un servicio para editar.")
            return

        servicio = tree.item(seleccionado[0], "values")
        servicio_id = servicio[0]

        form = tk.Toplevel(self.root)
        form.title("Editar Servicio Realizado")
        form.transient(self.root)
        form.grab_set()

        campos = ["cambio_toner", "cambio_ui", "cambio_fusor", "contador", "observaciones", "servicio_realizado"]
        entradas = []

        for i, campo in enumerate(campos):
            ttk.Label(form, text=campo.replace("_", " ").capitalize() + ":").grid(row=i, column=0, sticky="w", padx=5, pady=3)
            entry = ttk.Entry(form, width=50)
            entry.grid(row=i, column=1, padx=5, pady=3)
            entry.insert(0, servicio[i + 2])  # Ajustar si hay más columnas antes
            entradas.append(entry)

        ttk.Button(form, text="Guardar Cambios", command=lambda: self.guardar_edicion_servicio(servicio_id, entradas, form, tree)).grid(row=len(campos), columnspan=2, pady=10)

    def guardar_edicion_servicio(self, servicio_id, entradas, form, tree):
        datos = [e.get() for e in entradas]
        self.cursor.execute("""
            UPDATE servicios SET 
            cambio_toner=?, cambio_ui=?, cambio_fusor=?, contador=?, observaciones=?, servicio_realizado=?
            WHERE id=?
        """, (*datos, servicio_id))
        self.conn.commit()
        form.destroy()
        self.mostrar_servicios(tree.item(tree.selection()[0], "values")[1], tree)  # Actualiza la tabla
        messagebox.showinfo("Actualizado", "Servicio editado correctamente.")



if __name__ == "__main__":
    root = tk.Tk()
    app = GestionClientes(root)
    root.mainloop()