import sqlite3
from typing import final

class ProgramaPrincipal:
    
    def menu(self):
        while True:
            print("Monopatines\nMenú de opciones:\n")
            print("1- Cargar un monopatín")
            print("2- Modificar precio")
            print("3- Eliminar monopatín")
            print("4- Cargar disponibilidad")
            print("5- Mostrar listado de monopatines")
            print("-Ingrese 0 para salir-\n")
            nro = int(input("Por favor, ingrese una opción: \n"))
            if nro == 1:
                marca = input("Ingrese la marca del monopatín: ")
                precio = input("Ingrese el precio: ")
                cantidad = input("Ingrese la cantidad de unidades disponible: ")
                nuevo_monopatin = Monopatin(marca,precio,cantidad)
                nuevo_monopatin.cargar_monopatin()
            if nro == 2:
                id = input("Ingrese codigo del monopatín")
                precio = input("Ingrese el nuevo precio: ")
                monopatin_a_modificar = Monopatin(precio)
                monopatin_a_modificar.modificar_datos(id)
                # conexion = Conexiones()
                # conexion.abrirConexion()
                # try:
                #     conexion.miCursor.execute("UPDATE MONOPATINES SET precio='{}' where id_monopatin='{}'".format(preciom,id))
                # except:
                #     print("Error al actualizar precio")
                # finally:
                #     conexion.cerrarConexion()
            if nro == 4:
                marca = input("Ingrese marca del monopatín")
                monopatin_aumentar = Monopatin(marca)
                monopatin_aumentar.cargar_disponibilidad()
            if nro == 5:
                Monopatin.lista_monopatines()
                
    def crearTablas(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        conexion.miCursor.execute("DROP TABLE IF EXISTS MONOPATINES")
        conexion.miCursor.execute("CREATE TABLE MONOPATINES (id_monopatin INTEGER PRIMARY KEY ,marca VARCHAR(30), precio FLOAT NOT NULL, cantidad INTEGER NOT NULL, UNIQUE(marca))")
        conexion.miConexion.commit()
        conexion.cerrarConexion()
        
#clase principal 
class Monopatin:
    def __init__(self, marca, precio=None, cantidad=None):
        self.marca = marca
        self.precio = precio
        self.cantidad = cantidad
        
    def cargar_monopatin(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("INSERT INTO MONOPATINES(marca,precio,cantidad) VALUES('{}', '{}', '{}')".format(self.marca, self.precio, self.cantidad))
            conexion.miConexion.commit()
            print("Monopatín cargado exitosamente")
        except:
            print("Error al agregar el monopatín")
        finally:
            conexion.cerrarConexion()
    
    def modificar_datos(self,id):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("UPDATE MONOPATINES SET precio='{}' where idrow='{}'".format(self.precio,int(id)))
        except:
            print("Error al actualizar precio")
        finally:
            conexion.cerrarConexion()
    
    def cargar_disponibilidad(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("UPDATE MONOPATINES SET cantidad=cantidad+1 where marca='{}'".format(self.marca))
            conexion.miConexion.commit()
            print("Monopatín cargado exitosamente")
        except:
            print("Error al querer cargar unidad")
        finally:
            conexion.cerrarConexion()
    
    @classmethod
    def lista_monopatines(cls):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("SELECT * FROM MONOPATINES")
            monos = conexion.miCursor.fetchall()
            print("\ncodigo\t marca\tprecio\tcantidad")
            for mono in monos:
                id,marca,precio,cantidad = mono
                print(str(id),"\t",str(marca),"\t",str(precio),"\t",str(cantidad))
        except:
            print("Error al querer mostrar listado")
        finally:
            conexion.cerrarConexion()

#clase para las conexiones con la base de datos
class Conexiones:
    def abrirConexion(self):
        self.miConexion = sqlite3.connect("Monopatines")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()
        
programa = ProgramaPrincipal()
programa.crearTablas()
programa.menu()