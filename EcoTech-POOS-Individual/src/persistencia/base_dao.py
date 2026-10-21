import sqlite3
from abc import ABC, abstractmethod
import pymysql
from persistencia.conexion import abrir_conexion, marcador_sql

ERRORES_BD = (sqlite3.Error, pymysql.MySQLError, ValueError, OverflowError)


class BaseDAO(ABC):
    TABLA = ""
    COLUMNAS = ""
    NOMBRE = ""

    @staticmethod
    @abstractmethod
    def _convertir(fila):
        pass

    @staticmethod
    def _preparar(sql):
        return sql.replace("?", marcador_sql())

    @staticmethod
    def _ejecutar(sql, parametros, accion):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(BaseDAO._preparar(sql), parametros)
            conexion.commit()
            return cursor.rowcount
        except ERRORES_BD as e:
            print(f"Error al {accion}: {e}")
            if conexion is not None:
                conexion.rollback()
            return 0
        finally:
            if conexion is not None:
                conexion.close()

    @staticmethod
    def _insertar(sql, parametros, accion):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(BaseDAO._preparar(sql), parametros)
            conexion.commit()
            return cursor.lastrowid
        except ERRORES_BD as e:
            print(f"Error al {accion}: {e}")
            if conexion is not None:
                conexion.rollback()
            return None
        finally:
            if conexion is not None:
                conexion.close()

    @staticmethod
    def _consultar(sql, parametros, accion):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(BaseDAO._preparar(sql), parametros)
            return cursor.fetchall()
        except ERRORES_BD as e:
            print(f"Error al {accion}: {e}")
            return []
        finally:
            if conexion is not None:
                conexion.close()

    @classmethod
    def _listar_donde(cls, condicion, parametros, accion, orden="id"):
        sql = f"SELECT {cls.COLUMNAS} FROM {cls.TABLA} WHERE {condicion} ORDER BY {orden}"
        return [cls._convertir(fila) for fila in cls._consultar(sql, parametros, accion)]

    @classmethod
    def buscar_por_id(cls, id_buscado):
        sql = f"SELECT {cls.COLUMNAS} FROM {cls.TABLA} WHERE id = ?"
        filas = cls._consultar(sql, (id_buscado,), f"buscar {cls.NOMBRE}")
        if not filas:
            return None
        return cls._convertir(filas[0])

    @classmethod
    def listar_todos(cls):
        sql = f"SELECT {cls.COLUMNAS} FROM {cls.TABLA} ORDER BY id"
        return [cls._convertir(fila) for fila in cls._consultar(sql, (), f"listar {cls.TABLA}")]

    @classmethod
    def eliminar(cls, id_eliminar):
        sql = f"DELETE FROM {cls.TABLA} WHERE id = ?"
        return cls._ejecutar(sql, (id_eliminar,), f"eliminar {cls.NOMBRE}") > 0
