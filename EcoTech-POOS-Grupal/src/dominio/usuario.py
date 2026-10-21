class Usuario:
    def __init__(self, nombre: str, contraseña: str, rol: str, id_empleado: int = None, id = None):
        self.id = id
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.contraseña = None
        self.rol = rol
        self._registrado = False
        self._establecer_contraseña(contraseña)

    @classmethod
    def desde_bd(cls, id, nombre: str, contraseña_cifrada: str, rol: str, id_empleado: int = None):
        usuario = cls.__new__(cls)
        usuario.id = id
        usuario.id_empleado = id_empleado
        usuario.nombre = nombre
        usuario.contraseña = contraseña_cifrada
        usuario.rol = rol
        usuario._registrado = True
        return usuario
        
    def _establecer_contraseña(self, contraseña: str) -> None:
        from dominio.controlAcceso import ControlAcceso
        if not contraseña or len(contraseña) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        self.contraseña = ControlAcceso.cifrar_contraseña(contraseña)

    def registrar(self) -> bool:
        if not self.nombre or not self.contraseña or not self.rol:
            return False
        self._registrado = True
        return True
 
    def iniciar_sesion(self, contraseña_ingresada: str) -> bool:
        from dominio.controlAcceso import ControlAcceso
        if not self._registrado:
            return False
        return ControlAcceso.validar_credenciales(self, contraseña_ingresada)