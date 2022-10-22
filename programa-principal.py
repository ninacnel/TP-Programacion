# importamos las librerías "sqlite3" para trabajar con base de datos y "datetime" para usar elementos de tipo fecha 
import sqlite3 as sql 
import datetime 

# la clase principal del programa
class programa():
    def menu(self):
        while True:
            print("\nMenú de opciones:\n")
            print("1-Cargar monopatines")
            print("2-Modificar datos")
            print("3-Borrar un monopatín")
            print("4-Cargar disponibilidad")
            print("5-Listado de productos")
            print("6-Crear nueva tabla. Ingresar monopatín")
            print("7-Actualizar precio")
            print("8-Mostrar registros hasta fecha indicada")
            print("0-Salir del programa")
            opcion = int(input("\nIngrese una opción:\n"))                

            if opcion == 1: # pide los datos para luego guardarlos en las columnas correspondientes de la tabla "Monopatines"
                marca = str(input("Ingrese marca: "))
                precio = float(input("Ingrese precio: "))
                cantidad = int(input("Ingrese stock del producto: "))
                cargarMonopatines(marca,precio,cantidad)

            elif opcion == 2: # pide el id para actualizar el precio del monopatín
                nuevoId = int(input("Ingrese el código del monopatín que desea modificar: "))
                nuevoPrecio = float(input("Ingrese el nuevo precio: "))
                actualizarPrecio(nuevoPrecio, nuevoId)

            elif opcion == 3: # pide el id de un monopatín para eliminarlo
                nuevoId = int(input("Ingrese el código del monopatín que desea eliminar: "))
                borrarMonopatin(nuevoId)

            elif opcion == 4: # pide la marca y aumenta en 1 unidad la cantidad de ese producto
                nombreMarca = str(input("Ingrese la marca del monopatín a aumentar stock: "))
                cargarDisponibilidad(nombreMarca)

            elif opcion == 5: # muestra la información guardada en la tabla "Monopatín"
                leerTablaMonopatines()

            elif opcion == 6: # crea una nueva tabla llamada "Monopatin" y pide los datos correspondientes
                print("Ingrese los datos del monopatín para la nueva tabla")
                modelo = str(input("Ingrese modelo: "))
                marca = str(input("Ingrese marca: "))
                potencia = str(input("Ingrese potencia: "))
                precio = int(input("Ingrese precio: "))
                color = str(input("Ingrese color: "))
                anio = int(input("ESPECIFIQUE\nAÑO de ingreso del producto: "))
                mes = int(input("MES de ingreso del producto: "))
                dia = int(input("DÍA de ingreso del producto: "))
                fechaUltimoPrecio = datetime.datetime(anio, mes, dia)
                cargarRegistroNuevaTabla(modelo,marca,potencia,precio,color,fechaUltimoPrecio)

            elif opcion == 7: # copia los datos de "nuevaTabla" en la tabla "historicoPrecio", y luego aumenta un %23 el precio
                copiarTabla() 
                actualizarDolar() 
            
            elif opcion == 8: # pide por consola año, mes y dia para buscar los registros anteriores o con la misma fecha
                print("Para ver los registros anteriores a la fecha, ESPECIFIQUE:")
                anio = int(input("AÑO de ingreso del producto: "))
                mes = int(input("MES de ingreso del producto: "))
                dia = int(input("DÍA de ingreso del producto: "))
                fecha = datetime.datetime(anio, mes, dia)
                filtrarPorFecha(fecha)

            elif opcion == 0: # permite romper con el loop del while y se sale del programa
                print("Fin del programa.")
                break

 # método para crear la tabla "Monopatines" con cuatro columnas
def crearTabla():
    conexion = Conexiones()
    conexion.abrirConexion()
    conexion.miCursor.execute("DROP TABLE IF EXISTS Monopatines")
    conexion.miCursor.execute(
        """CREATE TABLE Monopatines (
        id INTEGER NOT NULL PRIMARY KEY,
        marca text UNIQUE,
        precio integer,
        cantidad integer
        )"""
    )
    conexion.miConexion.commit()
    conexion.cerrarConexion()

# método para crear la nueva tabla "Monopatin"        
def nuevaTabla(): 
    conexion = Conexiones()
    conexion.abrirConexion()
    conexion.miCursor.execute("DROP TABLE IF EXISTS Monopatin")
    conexion.miCursor.execute(
            """CREATE TABLE Monopatin (
            id_mono integer NOT NULL PRIMARY KEY,
            modelo varchar(30),
            marca varchar(30),
            potencia varchar(30),
            precio integer,
            color varchar(30),
            fechaUltimoPrecio datetime
            )""")
    conexion.miConexion.commit()
    conexion.cerrarConexion()

# método para crear la tabla "historicoPrecio" que va a contener la misma información que "nuevaTabla" pero con precio actualizado    
def historicoPrecio(): 
    conexion = Conexiones()
    conexion.abrirConexion()
    conexion.miCursor.execute("DROP TABLE IF EXISTS historicoPrecio")
    conexion.miCursor.execute(
            """CREATE TABLE historicoPrecio (
            id_mono integer NOT NULL PRIMARY KEY,
            modelo varchar(30),
            marca varchar(30),
            potencia varchar(30),
            precio integer,
            color varchar(30),
            fechaUltimoPrecio datetime
            )""")
    conexion.miConexion.commit()
    conexion.cerrarConexion()

# método para cargar datos en la tabla "Monopatines"
def cargarMonopatines(marca, precio, cantidad): 
    try:
        conexion = sql.connect("Monopatines")
        miCursor = conexion.cursor()
        instruccion = f"INSERT INTO Monopatines (marca,precio,cantidad) VALUES ('{marca}' , {precio} , {cantidad})"
        miCursor.execute(instruccion)
        conexion.commit()
        print("¡¡¡\nMonopatín cargado existosamente\n!!!")
    except:
        print("ERROR al cargar monopatin")
    finally:        
        conexion.close()

# método que muestra el contenido de la tabla "Monopatines"
def leerTablaMonopatines():
    conexion = Conexiones()
    conexion.abrirConexion()
    try:
        conexion.miCursor.execute("SELECT * FROM Monopatines")
        datos = conexion.miCursor.fetchall()
        print("\nLista de monopatines disponibles\ncódigo\t marca\t precio\tcantidad")
        for dato in datos:
                id,marca,precio,cantidad = dato
                print(str(id),"\t",str(marca),"\t",str(precio),"\t",str(cantidad))
    except:
        print("ERROR al querer mostrar listado")
    finally:
        conexion.cerrarConexion()

# método para modificar el precio según el id
def actualizarPrecio(nuevoPrecio,nuevoId): 
    try:
        conexion = sql.connect("Monopatines")
        miCursor = conexion.cursor()
        instruccion = f"UPDATE Monopatines SET precio={nuevoPrecio} WHERE id={nuevoId}"
        miCursor.execute(instruccion)
        conexion.commit()
        print("¡¡¡\nPrecio actualizado exitosamente\n!!!")
    except:
        print("ERROR al actualizar precio.")
    finally:
        conexion.close()

# método para eliminar un monopatín según el id
def borrarMonopatin(nuevoId):
    try:
        conexion = sql.connect("Monopatines")
        miCursor = conexion.cursor()
        instruction= f"DELETE from Monopatines where id={nuevoId}"
        miCursor.execute(instruction)
        conexion.commit()
        print("¡¡¡\nMonopatín eliminado exitosamente\n!!!")
    except:
        print("ERROR al borrar monopatin.")
    finally:
        conexion.close()
        
# método para incrementar la cantidad disponible de un monopatín según la marca
def cargarDisponibilidad(nombreMarca): 
    try:
        conexion = sql.connect("Monopatines")
        miCursor = conexion.cursor()
        instruccion = f"UPDATE Monopatines SET cantidad=cantidad+1 WHERE marca like '{nombreMarca}'"
        miCursor.execute(instruccion)
        conexion.commit()
        print("¡¡¡\nDisponibilidad cargada exitosamente\n!!!")
    except:
        print("ERROR al cargar unidad.")
    finally:
        conexion.close()

# método para cargar datos en "nuevaTabla"
def cargarRegistroNuevaTabla(modelo,marca,potencia,precio,color,fechaUltimoPrecio):
    try:
        conexion = sql.connect("Monopatines")
        miCursor = conexion.cursor()
        instruccion = f"INSERT INTO Monopatin (modelo,marca,potencia,precio,color,fechaUltimoPrecio) VALUES ('{modelo}', '{marca}' , '{potencia}' , {precio} , '{color}' , '{fechaUltimoPrecio}')"
        miCursor.execute(instruccion)
        conexion.commit()
        print("¡¡¡\nMonopatín cargado a nueva tabla exitosamente\n!!!")
    except:
        print("ERROR al cargar nuevo monopatin.")
    finally:
        conexion.close()

# método para copiar los todos(*) elementos de una "nuevaTabla" en "historicoPrecio"
def copiarTabla(): 
    try:
        conexion = sql.connect("Monopatines")
        miCursor = conexion.cursor()
        instruccion = f"INSERT INTO historicoPrecio SELECT * FROM Monopatin"
        miCursor.execute(instruccion)
        conexion.commit()
        print("Nueva Tabla creada exitosamente !!!")
    except:
        print("ERROR al copiar tabla.")
    finally:
        conexion.close()

# método para aumentar un %23 el precio de un monopatín
def actualizarDolar(): 
    try:
        conexion = sql.connect("Monopatines")
        miCursor = conexion.cursor()
        instruccion = f"UPDATE historicoPrecio SET precio=precio*1.23"
        miCursor.execute(instruccion)
        conexion.commit()
        print("¡¡¡\nPrecios actualizados exitosamente\n!!!")
    except:
        print("ERROR al actualizar precios.")
    finally:
        conexion.close()
        
# método que muestra los registros anteriores o de la misma fecha ingresada
def filtrarPorFecha(fecha):
    try:
        conexion = sql.connect("Monopatines")
        miCursor = conexion.cursor()
        instruccion = f"SELECT * FROM historicoPrecio WHERE fechaUltimoPrecio <= '{fecha}'"
        miCursor.execute(instruccion)
        datos = miCursor.fetchall()
        conexion.commit()
        print("\nTabla registro monopatines\ncódigo\t modelo\t marca\t potencia\tprecio\t color\t fecha")
        for dato in datos:
                id_mono,modelo,marca,potencia,precio,color,fechaUltimoPrecio = dato
                print(str(id_mono),"\t",str(modelo),"\t",str(marca),"\t",str(potencia),"\t",str(precio),"\t",str(color),"\t",(fechaUltimoPrecio))
    except:
        print("ERROR al filtrar por fechas.")
    finally:
        conexion.close()
              
# clase para las conexiones con la base de datos
class Conexiones:
    def abrirConexion(self):
        self.miConexion = sql.connect("Monopatines")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()

# creamos la tabla "Monopatines", la tabla "Monopatin" y a su vez la tabla "historicoPrecio"
crearTabla()
nuevaTabla()
historicoPrecio()
# ejecutamos el método "menu" de la clase "programa" mediante el objeto "prueba"
prueba = programa()
prueba.menu()