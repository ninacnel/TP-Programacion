from cgi import print_form
import sqlite3
from ssl import cert_time_to_seconds
from typing import final


class ProgramaPrincipal:

    def menu(self):
        opcion: int = 99
        while opcion != 0:
            print("MENU DE OPCIONES")
            print("1 - Cargar los monopatines")
            print("2 - Modificar precio de un monopatín")
            print("3 - Borrar un monopatin")
            print("4 - Cargar disponibilidad")
            print("5 - Listado de productos")
            print("6 - Tabla")
            print("7 - Tabla de precios=?=?=?")
            print("8 - Registros anteriores a una fecha en especifico de la tabla monopatin")
            print("9 - Primera y unica vez")
            print("0 - Salir")
            opcion = int(input("Ingrese una opcion: "))
            if opcion >= 0 and opcion <= 9:
                if opcion == 0:
                    break
                elif opcion == 1:
                    print("Carga de productos")
                    marca = str(input("Ingrese la marca del monopatin: "))
                    precio = float(input("Ingrese el precio del monopatín: "))
                    cantidad = int(input("Ingrese la cantidad disponible: "))
                    nuevo_monopatin = Monopatin(marca, precio, cantidad)
                    nuevo_monopatin.cargar_monopatin()
                elif opcion == 2:
                    print("Modificacion de precios")
                    marca = str(input("Ingrese la marca del monopatín: "))
                    precio = float(input("Ingrese el nuevo precio del monopatin: "))
                    monopatin_a_modificar = Monopatin(marca, precio, "")
                    monopatin_a_modificar.modificar_precio()
                elif opcion == 3:
                    print("Eliminacion de productos")
                    marca = str(input("Ingrese la marca del monopatín: "))

                    monopatin_a_eliminar=Monopatin(marca, "", "")
                    monopatin_a_eliminar.eliminar_monopatin()
                elif opcion == 4:
                    print("Cargar disponibilidad")
                    marca = str(input("Ingrese la marca del monopatín: "))
                    monopatin_a_aumentar_disponibilidad = Monopatin(marca, "", "") 
                    monopatin_a_aumentar_disponibilidad.cargar_disponibilidad()
                elif opcion == 5:
                    print("Listado de productos")
                    Monopatin.obtener_monopatines(self)
                elif opcion == 6:
                    tabla()
                elif opcion == 7:
                    tabla_historico_precios()
                elif opcion == 8:
                    registros_anteriores()
                else:
                    print("Opcion invalida - Ingrese un numero valido")
            else: 
                print("Opcion invalida - Ingrese un numero valido")

    def crearTablas(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        conexion.miCursor.execute("CREATE TABLE if not EXISTS monopatines( id integer primary key autoincrement, marca varchar(60) NOT NULL unique, precio REAL NOT NULL, cantidad int NOT NULL DEFAULT 0,disponibles int NOT NULL default 0)")
        conexion.cerrarConexion()

class Conexiones:
    def abrirConexion(self):
        self.miConexion = sqlite3.connect("sqlite.db")
        if self.miConexion is None:
            raise "Could not get connection"
        self.miCursor = self.miConexion.cursor()
    def cerrarConexion(self):
        self.miConexion.close()

class Monopatin:
    def cargar_monopatin(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"Insert into monopatines(marca,precio,cantidad) values('{self.marca}',{self.precio},{self.cantidad})")
            conexion.miConexion.commit()
            print("Monopatín cargado exitosamente")
        except:
            print("Error al agregar el monopatín")
        finally:
            conexion.cerrarConexion()

    def __init__(self,marca,precio, cantidad):
        self.marca = marca
        self.precio = precio
        self.cantidad = cantidad

    def cargar_disponibilidad(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"SELECT disponibles FROM monopatines WHERE marca='{self.marca}'")
            monopatinInDb = conexion.miCursor.fetchone()
            self.disponible = int(monopatinInDb[0]) + 1
            print(self.disponible, monopatinInDb)
            conexion.miCursor.execute(f"UPDATE monopatines SET disponibles={self.disponible} WHERE marca='{self.marca}'")
            conexion.miConexion.commit()
        except:
            print("Error al cargar la disponibilidad")
        finally:
            conexion.cerrarConexion()

    def obtener_monopatines(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("SELECT * FROM monopatines")
            listMon = conexion.miCursor.fetchall()
            for item in listMon:
                print(f"Marca del patin: {item[1]}")
                print(f"Precio del patin: {item[2]}")
                print(f"Cantidad disponibles del patin: {item[3]}")
        except:
            print("Error al querer mostrar el listado")
        finally:
            conexion.cerrarConexion()

    def modificar_precio(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"Update monopatines set precio={self.precio} where marca='{self.marca}'")
            conexion.miConexion.commit()
            print("Precio actualizado correctamente")
        except:
            print("Error al actualizar precio")
        finally:
            conexion.cerrarConexion()
    
    def eliminar_monopatin(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"DELETE FROM monopatines WHERE marca='{self.marca}'")
            conexion.miConexion.commit()
            print("Monopatin eliminado correctamente")
        except:
            print("Error al querer eliminar el producto")
        finally:
            conexion.cerrarConexion()
    
    def tabla(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("DROP TABLE IF EXISTS MONOPATINES")
            conexion.miCursor.execute("CREATE TABLE MONOPATIN (modelo (Varchar(30)), marca (Varchar(30)), potencia (Varchar(30)), precio(Integer), color (Varchar(30)), fechaUltimoPrecio (datetime))")
            conexion.miConexion.commit()
        finally:
            conexion.cerrarConexion()
    
    def tabla_historico_precios(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        conexion.miCursor.execute("CREATE TABLE historic_price AS SELECT * FROM monopatines")
        conexion.miCursor.execute("SELECT id, precio FROM monopatines")
        listMon = conexion.miCursor.fetchall()
        for item in listMon:
            precio = int(item[1]) + int(int(item[1]) * 0.23)
            conexion.miCursor.execute(f"UPDATE tablaname SET precio={precio} fechaUltimoPrecio={'16/10/2022'} WHERE id={id}")
        conexion.cerrarConexion()
    
    def fechas_anteriores(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        conexion.miCursor.execute("SELECT * FROM monopatin where fechaUltimoPrecio <= fechaElegida")
        conexion.cerrarConexion

menu = ProgramaPrincipal()
menu.crearTablas()
menu.menu()
