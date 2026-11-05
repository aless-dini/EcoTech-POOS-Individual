import math
from datetime import date, datetime


class Indicador:
    """Valor en pesos chilenos de un indicador (UF, UTM, dólar), tal como se conserva en EcoTech."""

    def __init__(self, fecha, valor, codigo="uf", unidad="CLP/UF", verificado_en=None,
                 fuente="api.cmfchile.cl", id=None):
        # Validar fecha ISO y valor numérico finito positivo.
        self.id = id
        self.fecha = fecha
        self.valor = valor
        self.fuente = fuente
        self.codigo = codigo
        self.unidad = unidad
        self.verificado_en = verificado_en

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = self.validar_fecha(valor)

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, numero):
        self._valor = self.validar_valor(numero)

    @property
    def fuente(self):
        return self._fuente

    @fuente.setter
    def fuente(self, texto):
        self._fuente = self.validar_texto(texto, "La fuente del indicador")

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, texto):
        texto = self.validar_texto(texto, "El código del indicador").lower()
        if not texto.isascii() or not texto.isalpha() or len(texto) > 10:
            raise ValueError("El código del indicador debe tener solo letras, por ejemplo uf.")
        self._codigo = texto

    @property
    def unidad(self):
        return self._unidad

    @unidad.setter
    def unidad(self, texto):
        texto = self.validar_texto(texto, "La unidad del indicador")
        if not texto.startswith("CLP/") or len(texto) > 10:
            raise ValueError("La unidad debe indicar pesos por unidad, por ejemplo CLP/UF.")
        self._unidad = texto

    @property
    def verificado_en(self):
        return self._verificado_en

    @verificado_en.setter
    def verificado_en(self, texto):
        # Momento en que se recibió una respuesta válida (AAAA-MM-DDTHH:MM:SS).
        if texto is not None:
            try:
                datetime.fromisoformat(texto)
            except (TypeError, ValueError):
                raise ValueError("La fecha de verificación no es válida.") from None
        self._verificado_en = texto

    @staticmethod
    def validar_texto(texto, campo):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError(f"{campo} es obligatorio.")
        return texto.strip()

    @staticmethod
    def validar_fecha(fecha):
        try:
            return date.fromisoformat(fecha).isoformat()
        except (TypeError, ValueError):
            raise ValueError("La fecha del indicador debe tener formato AAAA-MM-DD.") from None

    @staticmethod
    def validar_valor(valor):
        if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
            raise ValueError("El valor del indicador debe ser un número positivo.")
        return float(valor)
