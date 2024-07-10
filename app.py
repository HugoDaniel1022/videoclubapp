import tkinter
import tkinter.messagebox
import mysql.connector
import random

class App():
    def __init__(self):
        self.ventana = tkinter.Tk()
        self.conexion = mysql.connector.connect(host="localhost", user="root", password="", database="tienda")
        self.cursor = self.conexion.cursor()
        self.main()

    def refresh(self):
        for i in self.ventana.pack_slaves():
            i.destroy()
        for i in self.ventana.place_slaves():
            i.destroy()
        for i in self.ventana.grid_slaves():
            i.destroy()

    def actualizar_datos(self):
        self.cursor.execute(f"select * from users where nickname = '{self.datos[0][2]}'")
        self.datos = self.cursor.fetchall()

    def main(self):
        self.refresh()
        self.ventana.geometry("300x300+550+150")
        self.encabezado_main = tkinter.Label(self.ventana, text="App de VideoClub", width=20, bg="lightgreen", font=("Arial", 26)).pack()
        self.boton_is = tkinter.Button(self.ventana, text="Iniciar Sesion", width=15, font=("Arial", 16), command=self.login).place(x=60, y=75)
        self.boton_r = tkinter.Button(self.ventana, text="Registrarse", width=15, font=("Arial", 16), command=self.register).place(x=60, y=130)

    def login(self):
        self.refresh()
        self.encabezado_login = tkinter.Label(self.ventana, text="LOGIN", width=20, bg="lightblue", font=("Arial", 26)).pack()
        self.label_user = tkinter.Label(self.ventana, text="Username:", width=13, font=("Arial", 12)).place(x=85, y=70)
        self.entry_user = tkinter.Entry(self.ventana, font=("Arial", 12))
        self.entry_user.place(x=55, y=100, height=25)
        self.label_pass = tkinter.Label(self.ventana, text="Password:", width=13, font=("Arial", 12)).place(x=85, y=140)
        self.entry_pass = tkinter.Entry(self.ventana, font=("Arial", 12))
        self.entry_pass.place(x=55, y=170, height=25)
        self.boton_cancel_login = tkinter.Button(self.ventana, text="Cancelar",  width=8, font=("Arial", 12), command=self.main).place(x=60, y=220)
        self.boton_entrar = tkinter.Button(self.ventana, text="Entrar",  width=8, font=("Arial", 12), command=self.ingresar).place(x=160, y=220)

    def ingresar(self):
        self.cursor.execute(f"select * from users where nickname = '{self.entry_user.get()}' and pasword = '{self.entry_pass.get()}'")
        self.datos = self.cursor.fetchall()
        if len(self.datos) > 0:
            self.menu()
        else:
            tkinter.messagebox.showerror("Error", "Usuario y/o password incorrectos !")

    def menu(self):
        self.refresh()
        self.ventana.geometry("500x500")
        self.frame_datos = tkinter.Frame(self.ventana, width=500, height=300, bd=2, relief="solid").pack()
        self.frame_foto = tkinter.Frame(self.frame_datos, width=200, height=250, bd=2, relief="solid").place(x=30, y=30)
        self.rotulo_codigo = tkinter.Label(self.frame_datos, text="Codigo:", width=10, font=("Arial", 12)).place(x=240, y=50)
        self.datos_codigo = tkinter.Label(self.frame_datos, text=f"{self.datos[0][1]}", width=10, font=("Arial", 12)).place(x=340, y=50)
        self.rotulo_nickname = tkinter.Label(self.frame_datos, text="Nickname:", width=10, font=("Arial", 12)).place(x=240, y=100)
        self.datos_nickname = tkinter.Label(self.frame_datos, text=f"{self.datos[0][2]}", width=10, font=("Arial", 12)).place(x=340, y=100)
        self.rotulo_telefono = tkinter.Label(self.frame_datos, text="Telefono:", width=10, font=("Arial", 12)).place(x=240, y=150)
        self.datos_telefono = tkinter.Label(self.frame_datos, text=f"{self.datos[0][4]}", width=10, font=("Arial", 12))
        self.datos_telefono.place(x=340, y=150)
        self.boton_modif_tel = tkinter.Button(self.frame_datos, text="M", width=3, command=self.modificar_tel).place(x=460, y=148)
        self.rotulo_direccion = tkinter.Label(self.frame_datos, text="Direccion:", width=10, font=("Arial", 12)).place(x=240, y=200)
        self.datos_direccion = tkinter.Label(self.frame_datos, text=f"{self.datos[0][5]}", width=10, font=("Arial", 12))
        self.datos_direccion.place(x=340, y=200)
        self.boton_modif_dir = tkinter.Button(self.frame_datos, text="M", width=3, command=self.modificar_dir).place(x=460, y=198)
        self.boton_que_alquilo = tkinter.Button(self.frame_datos, text="¿ Tengo alquilado algo ?", width=30, command=self.quepelialquile).place(x=240, y=250)

        # self.frame_acciones = tkinter.Frame(self.ventana).grid(row=0, column=1)
        self.boton_vertodas = tkinter.Button(self.ventana, text="Ver todas", width=10, command=self.vertodas).place(x=50, y=320)
        self.boton_verdispo = tkinter.Button(self.ventana, text="Ver dispo", width=10, command=self.verdispo).place(x=50, y=360)
        self.boton_alquilar = tkinter.Button(self.ventana, text="Alquilar", width=10, command=self.alquilar)
        self.boton_alquilar.place(x=50, y=400)
        self.boton_devolver = tkinter.Button(self.ventana, text="Devolver", width=10, command=self.devolver).place(x=50, y=440)
        self.lista_pelis = tkinter.Listbox(self.ventana, width=40)
        self.lista_pelis.place(x=200, y=310)

        self.vertodas()

    def modificar_tel(self):
        self.ventana_emergente = tkinter.Tk()
        self.entry_input_tel = tkinter.Entry(self.ventana_emergente)
        self.entry_input_tel.pack()
        self.boton_ok_tel = tkinter.Button(self.ventana_emergente, text="Ok", command=self.update_tel).pack()

    def update_tel(self):
        self.cursor.execute(f"update users set telefono = '{self.entry_input_tel.get()}' where nickname = '{self.datos[0][2]}'")
        self.conexion.commit()
        self.datos_telefono.config(text=f"{self.entry_input_tel.get()}")
        tkinter.messagebox.showinfo("", "Telefono modificado correctamente !")
        self.ventana_emergente.destroy()

    def modificar_dir(self):
        self.ventana_emergente = tkinter.Tk()
        self.entry_input_dir = tkinter.Entry(self.ventana_emergente)
        self.entry_input_dir.pack()
        self.boton_ok_tel = tkinter.Button(self.ventana_emergente, text="Ok", command=self.update_dir).pack()

    def update_dir(self):
        self.cursor.execute(f"update users set direccion = '{self.entry_input_dir.get()}' where nickname = '{self.datos[0][2]}'")
        self.conexion.commit()
        self.datos_direccion.config(text=f"{self.entry_input_dir.get()}")
        tkinter.messagebox.showinfo("", "Direccion modificada correctamente !")
        self.ventana_emergente.destroy()

    def quepelialquile(self):
        self.actualizar_datos()
        if self.datos[0][6] == "L":
            tkinter.messagebox.showinfo("", "No alquilaste nada capo/a !")
        else:
            self.cursor.execute(f"select nombre from pelis where codigo = '{self.datos[0][7]}'")
            result_2 = self.cursor.fetchall()
            tkinter.messagebox.showinfo("", f"Alquilaste {result_2[0][0]} !")

    def vertodas(self):
        self.lista_pelis.delete(0, tkinter.END)
        self.boton_alquilar.config(state="disabled")
        self.cursor.execute("select codigo, nombre, genero from pelis")
        result = self.cursor.fetchall()
        for i in result:
            self.lista_pelis.insert(tkinter.END, i)
    
    def verdispo(self):
        self.lista_pelis.delete(0, tkinter.END)
        self.boton_alquilar.config(state="normal")
        self.cursor.execute("select codigo, nombre, genero from pelis where situacion = 'L'")
        result = self.cursor.fetchall()
        for i in result:
            self.lista_pelis.insert(tkinter.END, i)

    def alquilar(self):
        seleccion_index = self.lista_pelis.curselection()
        if len(seleccion_index) > 0:
            self.actualizar_datos()
            if self.datos[0][6] == "A":
                tkinter.messagebox.showerror("", "Ya tenes una peli alquilada !")
            else:
                datos_pelis = self.lista_pelis.get(seleccion_index)
                self.cursor.execute(f"update users set situacion = 'A', codigo_pelicula = '{datos_pelis[0]}' where nickname = '{self.datos[0][2]}'")
                self.cursor.execute(f"update pelis set situacion = 'A', codigo_user = '{self.datos[0][1]}' where codigo = '{datos_pelis[0]}'")
                self.conexion.commit()
                self.verdispo()
        else:
            tkinter.messagebox.showerror("", "Tenes que seleccionar una capo/a !")

    def devolver(self):
        self.actualizar_datos()
        if self.datos[0][6] == "L":
            tkinter.messagebox.showerror("", "No tenes peliculas para devolver")
        else:
            self.cursor.execute(f"update users set situacion = 'L', codigo_pelicula = null where nickname = '{self.datos[0][2]}'")
            self.cursor.execute(f"update pelis set situacion = 'L', codigo_user = null where codigo = '{self.datos[0][7]}'")
            self.conexion.commit()
            self.verdispo()

    def register(self):
        self.refresh()
        self.encabezado_register = tkinter.Label(self.ventana, text="REGISTRO", width=20, bg="yellow", font=("Arial", 26)).pack()
        self.label_nickname = tkinter.Label(self.ventana, text="Nickname:", width=10).place(x=40, y=75)
        self.entry_nickname = tkinter.Entry(self.ventana)
        self.entry_nickname.place(x=120, y=75)
        self.label_password = tkinter.Label(self.ventana, text="Password:", width=10).place(x=40, y=100)
        self.entry_password = tkinter.Entry(self.ventana)
        self.entry_password.place(x=120, y=100)
        self.label_telefono = tkinter.Label(self.ventana, text="Telefono:", width=10).place(x=40, y=125)
        self.entry_telefono = tkinter.Entry(self.ventana)
        self.entry_telefono.place(x=120, y=125)
        self.label_direccion = tkinter.Label(self.ventana, text="Direccion:", width=10).place(x=40, y=150)
        self.entry_direccion = tkinter.Entry(self.ventana)
        self.entry_direccion.place(x=120, y=150)
        self.boton_cancel_register = tkinter.Button(self.ventana, text="Cancelar", width=8, font=("Arial", 12), command=self.main).place(x=60, y=200)
        self.boton_enviar = tkinter.Button(self.ventana, text="Enviar", width=8, font=("Arial", 12), command=self.insertar).place(x=160, y=200)

    def insertar(self):
        self.cursor.execute(f"select * from users where nickname = '{self.entry_nickname.get()}'")
        result = self.cursor.fetchall()
        if len(result) > 0:
            tkinter.messagebox.showerror("Error", "Usuario ya existe !")
        else:
            sql = "insert into users (codigo, nickname, pasword, telefono, direccion, situacion) values (%s,%s,%s,%s,%s,%s)"
            val = ("c" + str(random.randint(0,9))+str(random.randint(0,9)), self.entry_nickname.get(), self.entry_password.get(), self.entry_telefono.get(), self.entry_direccion.get(), "L")
            self.cursor.execute(sql, val)
            self.conexion.commit()
            tkinter.messagebox.showinfo("Ok", "Usuario registrado con éxito !")
            self.login()

app1 = App()
app1.ventana.mainloop()
