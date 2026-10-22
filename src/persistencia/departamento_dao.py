from dominio.departamento import Departamento
from persistencia.base_dao import BaseDAO


class DepartamentoDAO(BaseDAO):
    TABLA = "departamento"
    COLUMNAS = "id, nombre, id_gerente"
    NOMBRE = "el departamento"

    @staticmethod
    def _convertir(fila):
        return Departamento(
            id=fila[0],
            nombre=fila[1],
            id_gerente=fila[2],
        )

    @classmethod
    def insertar(cls, departamento):
        sql = "INSERT INTO departamento (nombre, id_gerente) VALUES (?, ?)"
        nuevo_id = cls._insertar(sql, (departamento.nombre, departamento.id_gerente),
                                 "insertar el departamento")
        if nuevo_id is None:
            return None
        departamento.id = nuevo_id
        return departamento

    @classmethod
    def actualizar(cls, departamento):
        sql = "UPDATE departamento SET nombre = ?, id_gerente = ? WHERE id = ?"
        parametros = (departamento.nombre, departamento.id_gerente, departamento.id)
        return cls._ejecutar(sql, parametros, "actualizar el departamento") > 0

    @classmethod
    def buscar_por_nombre(cls, nombre):
        departamentos = cls._listar_donde("nombre = ?", (nombre,), "buscar el departamento por nombre")
        if not departamentos:
            return None
        return departamentos[0]
