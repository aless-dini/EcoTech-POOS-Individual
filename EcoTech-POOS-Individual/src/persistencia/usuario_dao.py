from dominio.usuario import Usuario
from persistencia.base_dao import BaseDAO


class UsuarioDAO(BaseDAO):
    TABLA = "usuario"
    COLUMNAS = "id, id_empleado, nombre, contraseña, rol"
    NOMBRE = "el usuario"

    @staticmethod
    def _convertir(fila):
        return Usuario.desde_bd(
            id=fila[0],
            id_empleado=fila[1],
            nombre=fila[2],
            contraseña_cifrada=fila[3],
            rol=fila[4],
        )

    @classmethod
    def insertar(cls, usuario):
        sql = "INSERT INTO usuario (id_empleado, nombre, contraseña, rol) VALUES (?, ?, ?, ?)"
        parametros = (usuario.id_empleado, usuario.nombre, usuario.contraseña, usuario.rol)
        nuevo_id = cls._insertar(sql, parametros, "insertar el usuario")
        if nuevo_id is None:
            return None
        usuario.id = nuevo_id
        return usuario

    @classmethod
    def actualizar(cls, usuario):
        sql = "UPDATE usuario SET id_empleado = ?, nombre = ?, contraseña = ?, rol = ? WHERE id = ?"
        parametros = (usuario.id_empleado, usuario.nombre, usuario.contraseña, usuario.rol, usuario.id)
        return cls._ejecutar(sql, parametros, "actualizar el usuario") > 0

    @classmethod
    def buscar_por_nombre(cls, nombre):
        usuarios = cls._listar_donde("nombre = ?", (nombre,), "buscar el usuario")
        if not usuarios:
            return None
        return usuarios[0]
