from dominio.registroTiempo import RegistroTiempo
from persistencia.base_dao import BaseDAO


class RegistroTiempoDAO(BaseDAO):
    TABLA = "registroTiempo"
    COLUMNAS = "id, id_empleado, id_proyecto, fecha, horasTrabajadas"
    NOMBRE = "el registro de tiempo"

    @staticmethod
    def _convertir(fila):
        return RegistroTiempo(
            id=fila[0],
            id_empleado=fila[1],
            id_proyecto=fila[2],
            fecha=fila[3],
            horas=fila[4],
        )

    @classmethod
    def insertar(cls, registro):
        sql = (
            "INSERT INTO registroTiempo (id_empleado, id_proyecto, fecha, horasTrabajadas) "
            "VALUES (?, ?, ?, ?)"
        )
        parametros = (registro.id_empleado, registro.id_proyecto, registro.fecha, registro.horas)
        nuevo_id = cls._insertar(sql, parametros, "insertar el registro de tiempo")
        if nuevo_id is None:
            return None
        registro.id = nuevo_id
        return registro

    @classmethod
    def actualizar(cls, registro):
        sql = (
            "UPDATE registroTiempo "
            "SET id_empleado = ?, id_proyecto = ?, fecha = ?, horasTrabajadas = ? "
            "WHERE id = ?"
        )
        parametros = (
            registro.id_empleado,
            registro.id_proyecto,
            registro.fecha,
            registro.horas,
            registro.id,
        )
        return cls._ejecutar(sql, parametros, "actualizar el registro de tiempo") > 0

    @classmethod
    def listar_por_empleado(cls, id_empleado):
        return cls._listar_donde("id_empleado = ?", (id_empleado,),
                                 "listar los registros de tiempo del empleado")

    @classmethod
    def listar_por_proyecto(cls, id_proyecto):
        return cls._listar_donde("id_proyecto = ?", (id_proyecto,),
                                 "listar los registros de tiempo del proyecto")
