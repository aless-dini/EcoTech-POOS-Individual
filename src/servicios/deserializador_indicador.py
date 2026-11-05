from dominio.indicador import Indicador
from servicios.api_cmf import FUENTE, INDICADORES, codigo_de, extraer_primero


class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos):
        # Reutiliza la función que extrae y valida los datos.
        fecha, valor = extraer_primero(datos)
        codigo = codigo_de(datos)

        # Construye y devuelve un objeto de nuestro proyecto.
        # No consulta la API ni guarda en la BD.
        _, unidad, _ = INDICADORES[codigo]
        return Indicador(fecha=fecha, valor=valor, codigo=codigo, unidad=unidad, fuente=FUENTE)
