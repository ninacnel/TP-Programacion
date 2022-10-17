import sqlite3
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
            print("7 - Tabla de precios historicos")
            print("8 - Registros anteriores")
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
                    print("Crear otra tabla de monopatines")
                    modelo = str(input("Ingrese el modelo"))
                    marca = str(input("Ingrese la marca"))
                    potencia = str(input("Ingrese la potencia"))
                    precio = (input("Ingrese el precio"))
                    color = str(input("Ingrese el color"))
                    fechaUltimoPrecio= str(input("Ingrese la fecha del ultimo precio"))
                    tablalol = Monopatin ()

                elif opcion == 7:
                    self.tabla_historico_precios()
                elif opcion == 8:
                    self.registros_anteriores()
                else:
                    print("Opcion invalida - Ingrese un numero valido")
            else: 
                print("Opcion invalida - Ingrese un numero valido")
    def crearTablas(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        conexion.miCursor.execute("CREATE TABLE IF NOT EXISTS MONOPATINES( id INTEGER PRIMARY KEY AUTOINCREMENT, marca VARCHAR(30) NOT NULL UNIQUE, precio REAL NOT NULL, cantidad INTEGER NOT NULL DEFAULT 0,disponibles INTEGER NOT NULL default 0)")
        conexion.cerrarConexion()
    
    def tabla(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        conexion.miCursor.execute("DROP TABLE IF EXISTS MONOPATINES")
        conexion.miCursor.execute("CREATE TABLE MONOPATIN (id_mono integer primary key autoincrement,modelo varchar(30),marca varchar(30),potencia varchar(30),precio int,color varchar(30), fechaUltimoPrecio datetime")
        conexion.miConexion.commit() 
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
    def __init__(self,modelo,marca,potencia,precio,color,fechaUltimoPrecio,cantidad):
        self.modelo = modelo
        self.cantidad = cantidad
        self.marca = marca
        self.potencia = potencia
        self.precio = precio
        self.color = color
        self.fechaUltimoPrecio = fechaUltimoPrecio
    def cargar_monopatin(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"INSERT INTO MONOPATINES(marca,precio,cantidad) values('{self.marca}',{self.precio},{self.cantidad})")
            conexion.miConexion.commit()
            print("Monopatín cargado exitosamente")
        except:
            print("Error al agregar el monopatín")
        finally:
            conexion.cerrarConexion()
    
    def cargar_monopatines(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"INSERT INTO MONOPATIN(modelo,marca,potencia,precio,color,fechaUltimoPrecio) values('{self.modelo},{self.marca}',{self.potencia},{self.precio},{self.color},{self.fechaUltimoPrecio})")
            conexion.miConexion.commit()
            print("Monopatín cargado exitosamente")
        except:
            print("Error al agregar el monopatín")
        finally:
            conexion.cerrarConexion()

    def cargar_disponibilidad(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"SELECT DISPONIBLES FROM MONOPATINES WHERE marca='{self.marca}'")
            monopatinInDb = conexion.miCursor.fetchone()
            self.disponible = int(monopatinInDb[0]) + 1
            print(self.disponible, monopatinInDb)
            conexion.miCursor.execute(f"UPDATE MONOPATINES SET DISPONIBLES={self.disponible} WHERE marca='{self.marca}'")
            conexion.miConexion.commit()
        except:
            print("Error al cargar la disponibilidad")
        finally:
            conexion.cerrarConexion()

    def obtener_monopatines(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("SELECT * FROM MONOPATINES")
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
            conexion.miCursor.execute(f"UPDATE MONOPATINES SET precio={self.precio} where marca='{self.marca}'")
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
            conexion.miCursor.execute(f"DELETE FROM MONOPATINES WHERE marca='{self.marca}'")
            conexion.miConexion.commit()
            print("Monopatin eliminado correctamente")
        except:
            print("Error al querer eliminar el producto")
        finally:
            conexion.cerrarConexion()

    
    
    def tabla_historico_precios(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("CREATE TABLE historic_price AS SELECT * FROM MONOPATINES")
            conexion.miCursor.execute("SELECT id, precio FROM MONOPATINES")
            listMon = conexion.miCursor.fetchall()
            for item in listMon:
                precio = int(item[1]) + int(int(item[1]) * 0.23)
                conexion.miCursor.execute(f"UPDATE MONOPATINES SET precio={precio} fechaUltimoPrecio={'16/10/2022'} WHERE id={id}")
                conexion.miConexion.commit()
        finally:
            conexion.cerrarConexion()
    
    def registros_anteriores(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("SELECT * FORM MONOPATIN where fechaUltimoPrecio <= fechaElegida")
            conexion.miConexion.commit()
        finally:
            conexion.cerrarConexion()
    
    

programa = ProgramaPrincipal()
programa.crearTablas()
programa.menu()
