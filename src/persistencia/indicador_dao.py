from dominio.indicador import Indicador
from persistencia.base_dao import BaseDAO
from persistencia.conexion import obtener_motor

# La clave de una observación es fuente + código + fecha del dato:
# consultar varias veces el mismo día actualiza la fila en vez de duplicarla.
SQL_GUARDAR_SQLITE = """
INSERT INTO indicador_api
    (fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
    valor = excluded.valor,
    unidad = excluded.unidad,
    verificado_en = excluded.verificado_en
"""

# MySQL y MariaDB (XAMPP) no tienen ON CONFLICT; esta es la forma equivalente.
SQL_GUARDAR_MYSQL = """
INSERT INTO indicador_api
    (fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (?, ?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE
    valor = VALUES(valor),
    unidad = VALUES(unidad),
    verificado_en = VALUES(verificado_en)
"""


class IndicadorDAO(BaseDAO):
    TABLA = "indicador_api"
    COLUMNAS = "id, fuente, codigo, fecha, valor, unidad, verificado_en"
    NOMBRE = "el indicador"

    @staticmethod
    def _convertir(fila):
        return Indicador(
            id=fila[0],
            fuente=fila[1],
            codigo=fila[2],
            fecha=fila[3],
            valor=fila[4],
            unidad=fila[5],
            verificado_en=fila[6],
        )

    @classmethod
    def guardar(cls, indicador):
        # Inserta la observación nueva o actualiza la existente; los datos van como parámetros.
        sql = SQL_GUARDAR_SQLITE if obtener_motor() == "sqlite" else SQL_GUARDAR_MYSQL
        parametros = (indicador.fuente, indicador.codigo, indicador.fecha,
                      indicador.valor, indicador.unidad, indicador.verificado_en)
        cls._ejecutar(sql, parametros, "guardar el indicador")
        return True

    @classmethod
    def listar(cls, codigo):
        # Del más reciente al más antiguo.
        return cls._listar_donde("codigo = ?", (codigo,), "leer el historial del indicador",
                                 orden="fecha DESC")

    @classmethod
    def buscar_ultimo(cls, codigo):
        historial = cls.listar(codigo)
        if not historial:
            return None
        return historial[0]
