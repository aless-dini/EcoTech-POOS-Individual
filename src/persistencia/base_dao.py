from abc import ABC, abstractmethod
from persistencia.conexion import abrir_conexion, marcador_sql
from persistencia.errores import ERRORES_BD, ErrorBaseDatos, registro, traducir


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
    def _correr(sql, parametros, accion, leer, confirmar):
        # Única función que abre la conexión: los errores se traducen a ErrorBaseDatos
        # y la capa de menús decide cómo mostrarlos.
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(BaseDAO._preparar(sql), parametros)
            resultado = leer(cursor)
            if confirmar:
                conexion.commit()
            return resultado
        except ERRORES_BD as e:
            if conexion is not None and confirmar:
                try:
                    conexion.rollback()
                except ERRORES_BD:
                    registro.warning("No se pudo deshacer la operación al %s", accion)
            raise traducir(e, accion) from e
        finally:
            if conexion is not None:
                conexion.close()

    @staticmethod
    def _ejecutar(sql, parametros, accion):
        return BaseDAO._correr(sql, parametros, accion, lambda cursor: cursor.rowcount, True)

    @staticmethod
    def _insertar(sql, parametros, accion):
        return BaseDAO._correr(sql, parametros, accion, lambda cursor: cursor.lastrowid, True)

    @staticmethod
    def _consultar(sql, parametros, accion):
        return BaseDAO._correr(sql, parametros, accion, lambda cursor: cursor.fetchall(), False)

    @classmethod
    def _convertir_filas(cls, filas):
        # Las clases del dominio validan sus datos; si algo guardado no cumple
        # las reglas, se informa en vez de cerrar el programa.
        try:
            return [cls._convertir(fila) for fila in filas]
        except (TypeError, ValueError):
            registro.error("Datos inválidos en la tabla %s", cls.TABLA, exc_info=True)
            raise ErrorBaseDatos(f"Hay datos guardados en la tabla {cls.TABLA} que no cumplen las reglas del sistema.") from None

    @classmethod
    def _listar_donde(cls, condicion, parametros, accion, orden="id"):
        sql = f"SELECT {cls.COLUMNAS} FROM {cls.TABLA} WHERE {condicion} ORDER BY {orden}"
        return cls._convertir_filas(cls._consultar(sql, parametros, accion))

    @classmethod
    def buscar_por_id(cls, id_buscado):
        sql = f"SELECT {cls.COLUMNAS} FROM {cls.TABLA} WHERE id = ?"
        filas = cls._consultar(sql, (id_buscado,), f"buscar {cls.NOMBRE}")
        if not filas:
            return None
        return cls._convertir_filas(filas[:1])[0]

    @classmethod
    def listar_todos(cls):
        sql = f"SELECT {cls.COLUMNAS} FROM {cls.TABLA} ORDER BY id"
        return cls._convertir_filas(cls._consultar(sql, (), f"listar {cls.TABLA}"))

    @classmethod
    def eliminar(cls, id_eliminar):
        sql = f"DELETE FROM {cls.TABLA} WHERE id = ?"
        return cls._ejecutar(sql, (id_eliminar,), f"eliminar {cls.NOMBRE}") > 0
