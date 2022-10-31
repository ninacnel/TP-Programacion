# método para aumentar un %23 el precio de un monopatín
# def actualizarDolar():
#     conexion = sql.connect("Monopatines.db")
#     miCursor = conexion.cursor()
#     try:
#         instruccion = f"UPDATE historicoPrecio SET precio=precio*1.23" # que actualice monopatin
#         miCursor.execute(instruccion)
#         conexion.commit()
#         print("¡¡¡\nPrecios actualizados exitosamente\n!!!")
#     except:
#         print("ERROR al actualizar precios.")
#     finally:
#         conexion.close()