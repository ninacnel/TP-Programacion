# importamos las librerías "sqlite3" para trabajar con base de datos y "datetime" para usar elementos de tipo fecha 
import sqlite3 as sql 
import datetime 

# la clase principal del programa
class programa():
    #Metodo menú,que llama funciones externas para poder realizar las diferentes órdenes.
    def menu(self):
        while True:
            #Opciones que nos brinda el menú.
            print("\nMenú de opciones:\n")
            print("1-Cargar monopatín.")
            print("2-Modificar un precio.")
            print("3-Borrar un registro.")
            print("4-Cargar disponibilidad.")
            print("5-Listar productos.")
            print("6-Crear nueva tabla personalizada. Ingresar registros a la tabla.")
            print("7-Aumentar precio.")
            print("8-Mostrar todos los registros.")
            print("0-Salir del programa.")
            #Carga de la variable "opcion", que nos permite actuar como el operador para la estructura SWITCH/CASE(creada por Ifs).
            opcion = int(input("\nIngrese una opción:\n"))                

            if opcion == 1: #Opción 1- Cargamos 3 variables y las pasamos como parámetros en la función para cargar un registro completo para la tabla "Monopatines", en nuestra base de datos.
                marca = str(input("Inserte el nombre de la marca:"))
                precio = float(input("Inserte el precio del producto:"))
                cantidad = int(input("Inserte la cantidad en stock del producto:"))
                insertarRegistro(marca,precio,cantidad)

            elif opcion == 2: #Opción 2- Solicitamos un Id como variable y un nuevo precio. Comparamos el Id con el que se encuentra en la base de Datos.Si se encuentra, reemplaza el precio anterior por el nuevo.
                nuevoId = int(input("Ingrese el id del producto que desea modificar:\n"))
                nuevoPrecio = float(input("Ingrese el nuevo valor del producto seleccionado:\n"))
                actualizarPrecio(nuevoPrecio, nuevoId)

            elif opcion == 3: #Opción 3- Borra un registro en base a un Id que le pasamos por consola.
                nuevoId = int(input("Ingrese el id del producto que desea borrar:\n"))
                borrarMonopatin(nuevoId)

            elif opcion == 4: #Opción 4- Pasamos por consola una variable con la marca, si hay una parecida o igual en la BD, aumentamos el stock en 1.
                nombreMarca = str(input("Ingrese el nombre de la marca a la que desa aumentar el stock:"))
                cargarDisponibilidad(nombreMarca)

            elif opcion == 5: #Opción 5- Permite visualizar una de las tres tablas creadas. Es necesario escribir el nombre de la tabla para que se muetren en pantalla.
                leerTablaMonopatines()

            elif opcion == 6: #Opción 6- Crea un con nuevas columnas para una nueva tabla llamada "Monopatin".
                print("Ingrese los datos de un producto a la nueva tabla.")
                modelo = str(input("Ingrese el modelo:"))
                marca = str(input("Ingrese la marca:"))
                potencia = str(input("Ingrese la potencia:"))
                precio = int(input("Ingrese el precio:"))
                color = str(input("Ingrese el color:"))
                anio = int(input("Ingrese el año de ingreso del producto:"))
                mes = int(input("Ingrese el mes de ingreso del producto:"))
                dia = int(input("Ingrese el día de ingreso del producto:"))
                fechaUltimoPrecio = datetime.datetime(anio, mes, dia)
                cargarRegistroNuevaTabla(modelo,marca,potencia,precio,color,fechaUltimoPrecio)

            elif opcion == 7: # Opción 7- Inserta los datos de "nuevaTabla" en la tabla "historicoPrecio", y luego aumenta un %23 el precio
                clonarTabla() 
                actualizarDolar() 
            
            elif opcion == 8: # Opción 8- Creamos variables para año, mes y día, que luego utilizamos para pasar como parámetro de tipo fecha en la función. Nos muestra los registros que tengan una fecha anterior a la que fue pasada como parámetro.
            #LA OPCIÓN Nº8 REQUIERE DE FORMA OBLIGATORIA HABER UTILIZADO LA OPCIÓN Nº7.DE LO CONTRARIO NOS MOSTRARÁ UNA LISTA VACÍA.
                anio = int(input("Ingrese el año de ingreso del producto:"))
                mes = int(input("Ingrese el mes de ingreso del producto:"))
                dia = int(input("Ingrese el día de ingreso del producto:"))
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

def insertarRegistro(marca, precio, cantidad): #Inserta los datos de cada uno de los parámetros en una columna específica de la tabla "Monopatines".
    try:
        conn = sql.connect("Monopatines")
        cursor = conn.cursor()
        instruccion = f"INSERT INTO Monopatines (marca,precio,cantidad) VALUES ('{marca}' , {precio} , {cantidad})"
        cursor.execute(instruccion)
        conn.commit()
        print("¡¡¡\nMonopatín cargado existosamente.\n!!!")
    except:
        print("ERROR al cargar monopatin")
    finally:        
        conn.close()

def leerTablaMonopatines():
    conexion = Conexiones()
    conexion.abrirConexion()
    try:
        conexion.miCursor.execute("SELECT * FROM Monopatines")
        datos = conexion.miCursor.fetchall()
        print("\ncodigo\t marca\tprecio\tcantidad")
        for dato in datos:
                id,marca,precio,cantidad = dato
                print(str(id),"\t",str(marca),"\t",str(precio),"\t",str(cantidad))
    except:
        print("Error al querer mostrar listado")
    finally:
        conexion.cerrarConexion()

def actualizarPrecio(nuevoPrecio,nuevoId): #Si encuentra una similitud de ID, nos permite modificar el precio de un producto en el regisro que posee ese ID.
    try:
        conn = sql.connect("Monopatines")
        cursor = conn.cursor()
        instruccion = f"UPDATE Monopatines SET precio={nuevoPrecio} WHERE id={nuevoId}"
        cursor.execute(instruccion)
        conn.commit()
        print("Precio actualizado exitosamente.")
    except:
        print("ERROR al actualizar precio.")
    finally:
        conn.close()

def borrarMonopatin(nuevoId): #Borra un registro en particular de la tabla selecionada.
    try:
        conn = sql.connect("Monopatines")
        cursor = conn.cursor()
        instruction= f"DELETE from Monopatines where id={nuevoId}"
        cursor.execute(instruction)
        conn.commit()
        print("Monopatín eliminado exitosamente.")
    except:
        print("ERROR al borrar monopatin.")
    finally:
        conn.close()
        

def cargarDisponibilidad(nombreMarca): #Incrementa la cantidad del stock en 1 del monopatín que pasemos la "marca" por consola.
    try:
        conn = sql.connect("Monopatines")
        cursor = conn.cursor()
        instruccion = f"UPDATE Monopatines SET cantidad=cantidad+1 WHERE marca like '{nombreMarca}'"
        cursor.execute(instruccion)
        conn.commit()
        print("¡¡¡\nDisponibilidad cargada exitosamente.\n!!!")
    except:
        print("ERROR al cargar unidad.")
    finally:
        conn.close()

def cargarRegistroNuevaTabla(modelo,marca,potencia,precio,color,fechaUltimoPrecio): #Crea un registro y almacena los datos de los parámetros en la columna correspondiente.
    try:
        conn = sql.connect("Monopatines")
        cursor = conn.cursor()
        instruccion = f"INSERT INTO Monopatin (modelo,marca,potencia,precio,color,fechaUltimoPrecio) VALUES ('{modelo}', '{marca}' , '{potencia}' , {precio} , '{color}' , '{fechaUltimoPrecio}')"
        cursor.execute(instruccion)
        conn.commit()
    except:
        print("ERROR al cargar nuevo monopatin.")
    finally:
        conn.close()

def clonarTabla(): #Clona todas las columnas de la tabla "Monopatin" y crea una nueva tabla con dichas columnas.
    try:
        conn = sql.connect("Monopatines")
        cursor = conn.cursor()
        instruccion = f"INSERT INTO historicoPrecio SELECT * FROM Monopatin"
        cursor.execute(instruccion)
        conn.commit()
    except:
        print("ERROR al clonar tablas.")
    finally:
        conn.close()

def actualizarDolar(): #Actualiza el precio incrementándolo en 0.23% del total anterior.
    try:
        conn = sql.connect("Monopatines")
        cursor = conn.cursor()
        instruccion = f"UPDATE historicoPrecio SET precio=precio*1.23"
        cursor.execute(instruccion)
        conn.commit()
        print("¡¡¡\nPrecios actualizados exitosamente.\n!!!")
    except:
        print("ERROR al actualizar precios.")
    finally:
        conn.close()

def filtrarPorFecha(fecha): #Hace una comparación de fechas y nos muestra los registro que posean una fecha anterior.
    try:
        conn = sql.connect("Monopatines")
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM historicoPrecio WHERE fechaUltimoPrecio <= '{fecha}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        print("\ncodigo\t modelo\t marca\t potencia\tprecio\t color\t fecha")
        for dato in datos:
                id_mono,modelo,marca,potencia,precio,color,fechaUltimoPrecio = dato
                print(str(id_mono),"\t",str(modelo),"\t",str(marca),"\t",str(potencia),"\t",str(precio),"\t",str(color),"\t",(fechaUltimoPrecio))
    except:
        print("ERROR al filtrar por fechas.")
    finally:
        conn.close()
        
        
# clase para las conexiones con la base de datos
class Conexiones:
    def abrirConexion(self):
        self.miConexion = sql.connect("Monopatines")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()

Ejecutar = programa()
# creamos la tabla "Monopatines", la tabla "Monopatin" y a su vez la tabla "historicoPrecio"
crearTabla()
nuevaTabla()
historicoPrecio()
# ejecutamos el método "menu" de la clase "programa" a través del objeto "Ejecutar"
Ejecutar.menu()