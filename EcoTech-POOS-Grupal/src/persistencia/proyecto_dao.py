from dominio.proyecto import Proyecto
from persistencia.base_dao import BaseDAO


class ProyectoDAO(BaseDAO):
    TABLA = "proyecto"
    COLUMNAS = "id, nombre, descripcion, fechaInicio"
    NOMBRE = "el proyecto"

    @staticmethod
    def _convertir(fila):
        return Proyecto(
            id=fila[0],
            nombre=fila[1],
            descripcion=fila[2],
            fechaInicio=fila[3],
        )

    @classmethod
    def insertar(cls, proyecto):
        sql = "INSERT INTO proyecto (nombre, descripcion, fechaInicio) VALUES (?, ?, ?)"
        parametros = (proyecto.nombre, proyecto.descripcion, proyecto.fechaInicio)
        nuevo_id = cls._insertar(sql, parametros, "insertar el proyecto")
        if nuevo_id is None:
            return None
        proyecto.id = nuevo_id
        return proyecto

    @classmethod
    def actualizar(cls, proyecto):
        sql = "UPDATE proyecto SET nombre = ?, descripcion = ?, fechaInicio = ? WHERE id = ?"
        parametros = (proyecto.nombre, proyecto.descripcion, proyecto.fechaInicio, proyecto.id)
        return cls._ejecutar(sql, parametros, "actualizar el proyecto") > 0

    @classmethod
    def asignar_empleado(cls, id_proyecto, id_empleado):
        sql = "INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (?, ?)"
        return cls._ejecutar(sql, (id_empleado, id_proyecto),
                             "asignar el empleado al proyecto") > 0

    @classmethod
    def quitar_empleado(cls, id_proyecto, id_empleado):
        sql = "DELETE FROM empleado_proyecto WHERE id_empleado = ? AND id_proyecto = ?"
        return cls._ejecutar(sql, (id_empleado, id_proyecto),
                             "quitar el empleado del proyecto") > 0

    @classmethod
    def listar_por_empleado(cls, id_empleado):
        columnas = ", ".join(f"p.{c.strip()}" for c in cls.COLUMNAS.split(","))
        sql = (
            f"SELECT {columnas} FROM proyecto p "
            "JOIN empleado_proyecto ep ON ep.id_proyecto = p.id "
            "WHERE ep.id_empleado = ? ORDER BY p.id"
        )
        filas = cls._consultar(sql, (id_empleado,), "listar los proyectos del empleado")
        return [cls._convertir(fila) for fila in filas]
