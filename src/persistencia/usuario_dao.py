from dominio.usuario import Usuario
from persistencia.base_dao import BaseDAO


class UsuarioDAO(BaseDAO):
    TABLA = "usuario"
    COLUMNAS = "id, id_empleado, nombre_usuario, password_hash, rol"
    NOMBRE = "el usuario"

    @staticmethod
    def _convertir(fila):
        return Usuario(
            id=fila[0],
            id_empleado=fila[1],
            nombre_usuario=fila[2],
            password_hash=fila[3],
            rol=fila[4],
        )

    @classmethod
    def insertar(cls, usuario):
        sql = "INSERT INTO usuario (id_empleado, nombre_usuario, password_hash, rol) VALUES (?, ?, ?, ?)"
        parametros = (usuario.id_empleado, usuario.nombre_usuario, usuario.password_hash, usuario.rol)
        nuevo_id = cls._insertar(sql, parametros, "insertar el usuario")
        if nuevo_id is None:
            return None
        usuario.id = nuevo_id
        return usuario

    @classmethod
    def actualizar(cls, usuario):
        sql = "UPDATE usuario SET id_empleado = ?, nombre_usuario = ?, password_hash = ?, rol = ? WHERE id = ?"
        parametros = (usuario.id_empleado, usuario.nombre_usuario, usuario.password_hash, usuario.rol, usuario.id)
        return cls._ejecutar(sql, parametros, "actualizar el usuario") > 0

    @classmethod
    def eliminar(cls, id_usuario):
        sql = "DELETE FROM usuario WHERE id = ?"
        return cls._ejecutar(sql, (id_usuario,), "eliminar el usuario") > 0

    @classmethod
    def listar_todos(cls):
        sql = f"SELECT {cls.COLUMNAS} FROM usuario ORDER BY id"
        return [cls._convertir(fila) for fila in cls._consultar(sql, (), "listar los usuarios")]

    @classmethod
    def buscar_por_id(cls, id_usuario):
        sql = f"SELECT {cls.COLUMNAS} FROM usuario WHERE id = ?"
        filas = cls._consultar(sql, (id_usuario,), "buscar el usuario")
        if not filas:
            return None
        return cls._convertir(filas[0])

    @classmethod
    def buscar_por_nombre(cls, nombre_usuario):
        usuarios = cls._listar_donde("nombre_usuario = ?", (nombre_usuario,), "buscar el usuario")
        if not usuarios:
            return None
        return usuarios[0]

    @classmethod
    def buscar_por_empleado(cls, id_empleado):
        usuarios = cls._listar_donde("id_empleado = ?", (id_empleado,), "buscar el usuario del empleado")
        if not usuarios:
            return None
        return usuarios[0]
