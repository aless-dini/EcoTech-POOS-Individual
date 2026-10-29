import logging
import sqlite3
import pymysql

registro = logging.getLogger("ecotech.bd")

ERRORES_BD = (sqlite3.Error, pymysql.MySQLError, OverflowError)


class ErrorBaseDatos(Exception):
    """Error de la base de datos con un mensaje apto para mostrar al usuario."""


def traducir(error, accion):
    # El detalle técnico va al log; al usuario solo le llega el mensaje claro.
    registro.error("Error al %s", accion, exc_info=error)

    if isinstance(error, (sqlite3.IntegrityError, pymysql.IntegrityError)):
        mensaje = "el dato ya existe o está relacionado con otros registros"
    elif isinstance(error, (pymysql.OperationalError, sqlite3.OperationalError)):
        mensaje = "no hay conexión con la base de datos o está ocupada, intente nuevamente"
    elif isinstance(error, (sqlite3.DataError, pymysql.DataError, OverflowError)):
        mensaje = "algún dato es demasiado grande o tiene un formato no válido"
    else:
        mensaje = "ocurrió un error inesperado en la base de datos"
    return ErrorBaseDatos(f"No fue posible {accion}: {mensaje}.")
