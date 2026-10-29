import re
from dominio.validaciones import SOLO_LETRAS, validar_texto, validar_fecha, validar_id_opcional

class Empleado:
    MAX_TEXTO = 100
    MIN_TELEFONO = 8
    MAX_TELEFONO = 9
    SALARIO_MIN = 100_000
    SALARIO_MAX = 50_000_000
    PATRON_CORREO = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

    def __init__(self, nombre: str, direccion: str, telefono: int, correo: str, salario: int, inicioContrato: str, id_departamento: int = None, id = None):
        self.id = id
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.salario = salario
        self.inicioContrato = inicioContrato

    @classmethod
    def validar_nombre(cls, nombre):
        return validar_texto(nombre, "El nombre", cls.MAX_TEXTO, minimo=2, caracteres=SOLO_LETRAS)

    @classmethod
    def validar_direccion(cls, direccion):
        return validar_texto(direccion, "La dirección", cls.MAX_TEXTO, minimo=3)

    @classmethod
    def validar_telefono(cls, telefono):
        texto = str(telefono).strip()
        if not (texto.isdecimal() and texto.isascii() and cls.MIN_TELEFONO <= len(texto) <= cls.MAX_TELEFONO):
            raise ValueError(f"El teléfono debe tener solo números, entre {cls.MIN_TELEFONO} y {cls.MAX_TELEFONO} dígitos.")
        return int(texto)

    @classmethod
    def validar_correo(cls, correo):
        correo = validar_texto(correo, "El correo", cls.MAX_TEXTO)
        if not cls.PATRON_CORREO.fullmatch(correo):
            raise ValueError("El correo no es válido (ejemplo: nombre@dominio.cl).")
        return correo

    @classmethod
    def validar_salario(cls, salario):
        try:
            salario = int(str(salario).strip())
        except ValueError:
            raise ValueError("El salario debe ser un número entero.") from None
        if not cls.SALARIO_MIN <= salario <= cls.SALARIO_MAX:
            raise ValueError(f"El salario debe estar entre {cls.SALARIO_MIN:,} y {cls.SALARIO_MAX:,}.".replace(",", "."))
        return salario

    @staticmethod
    def validar_inicio_contrato(fecha):
        return validar_fecha(fecha, "La fecha de inicio de contrato")

    @property
    def id_departamento(self):
        return self._id_departamento

    @id_departamento.setter
    def id_departamento(self, valor):
        self._id_departamento = validar_id_opcional(valor, "El id del departamento")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_nombre(valor)

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        self._direccion = self.validar_direccion(valor)

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = self.validar_telefono(valor)

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = self.validar_correo(valor)

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        self._salario = self.validar_salario(valor)

    @property
    def inicioContrato(self):
        return self._inicioContrato

    @inicioContrato.setter
    def inicioContrato(self, valor):
        self._inicioContrato = self.validar_inicio_contrato(valor)

    def mostrar_datos(self) -> str:
        return f"\nId {self.id}, Nombre {self.nombre}, Correo {self.correo}"

    def actualizar_nombre(self, nombre):
        self.nombre = nombre

    def agregar_descripcion(self) -> str:
        return (f"Empleado {self.nombre} (ID {self.id}) - {self.correo}\n"
                f"Dirección: {self.direccion} | Teléfono: {self.telefono}\n"
                f"Salario: {self.salario} | Inicio contrato: {self.inicioContrato} | "
                f"Departamento: {self.id_departamento if self.id_departamento is not None else 'Sin departamento'}")
