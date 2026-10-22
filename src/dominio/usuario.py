class Usuario:
    MIN_USUARIO = 3
    MAX_USUARIO = 40
    MIN_CLAVE = 8
    ROLES = ("administrador", "empleado")

    def __init__(self, nombre_usuario: str, password_hash: str, id_empleado: int, rol: str = "empleado", id = None):
        if type(id_empleado) is not int or id_empleado <= 0:
            raise ValueError("El ID del empleado debe ser positivo.")
        if rol not in self.ROLES:
            raise ValueError(f"El rol debe ser uno de estos: {', '.join(self.ROLES)}.")
        self.id = id
        self.id_empleado = id_empleado
        self.nombre_usuario = self.normalizar_usuario(nombre_usuario)
        self.password_hash = password_hash
        self.rol = rol

    @classmethod
    def normalizar_usuario(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El usuario debe ser texto.")
        nombre = nombre.strip().lower()
        if not cls.MIN_USUARIO <= len(nombre) <= cls.MAX_USUARIO:
            raise ValueError(f"El usuario debe tener entre {cls.MIN_USUARIO} y {cls.MAX_USUARIO} caracteres.")
        if not all(c.isascii() and (c.isalnum() or c == "_") for c in nombre):
            raise ValueError("Use letras sin tilde, números o guion bajo.")
        return nombre

    @classmethod
    def validar_clave(cls, clave):
        if not isinstance(clave, str):
            raise TypeError("La contraseña debe ser texto.")
        if len(clave) < cls.MIN_CLAVE:
            raise ValueError(f"Use al menos {cls.MIN_CLAVE} caracteres.")
        return clave  # Sin strip, lower ni truncado.

    @classmethod
    def validar_rol(cls, rol):
        rol = rol.strip().lower()
        if rol not in cls.ROLES:
            raise ValueError(f"El rol debe ser uno de estos: {', '.join(cls.ROLES)}.")
        return rol
