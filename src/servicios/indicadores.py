from datetime import date, datetime
import requests
from persistencia.errores import ErrorBaseDatos
from persistencia.indicador_dao import IndicadorDAO
from servicios.api_cmf import obtener_datos, validar_codigo
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.permisos import exigir_sesion

ORIGEN_API = "API"
ORIGEN_BD = "BD local"


def consultar_indicador(sesion, codigo):
    """Devuelve (dato, origen, mensaje). dato es None si no hay API ni respaldo."""
    exigir_sesion(sesion)
    codigo = validar_codigo(codigo)
    try:
        datos = obtener_datos(codigo)
        dato = DeserializadorIndicador.desde_api(datos)
    except (requests.exceptions.RequestException, ConnectionError,
            ValueError, KeyError, TypeError) as error:
        return buscar_respaldo(codigo, f"Servicio no disponible o respuesta inválida: {error}")

    # Última verificación: el momento en que recibimos una respuesta válida.
    dato.verificado_en = datetime.now().isoformat(timespec="seconds")

    # Intentar guardar. Si falla la BD, se informa ese fallo pero el dato de la API se muestra igual.
    try:
        IndicadorDAO.guardar(dato)
        mensaje = "Dato guardado en la BD local."
    except ErrorBaseDatos as error:
        mensaje = f"El dato no pudo guardarse: {error}"
    return dato, ORIGEN_API, mensaje


def buscar_respaldo(codigo, motivo):
    # Si no hay respaldo, no se inventa un dato ni se presenta como actualizado.
    try:
        ultimo = IndicadorDAO.buscar_ultimo(codigo)
    except ErrorBaseDatos as error:
        return None, None, f"{motivo}\nTampoco se pudo leer la BD local: {error}"
    if ultimo is None:
        return None, None, f"{motivo}\nNo hay datos guardados de {codigo.upper()} para usar como respaldo."
    return ultimo, ORIGEN_BD, f"{motivo}\nSe muestra el último dato guardado (respaldo)."


def obtener_historial(sesion, codigo):
    # Lee solo la BD: no llama a la API.
    exigir_sesion(sesion)
    return IndicadorDAO.listar(validar_codigo(codigo))


def uf_vigente(sesion):
    """La UF cambia una vez al día: si la de hoy ya está guardada, no se vuelve a llamar a la API."""
    exigir_sesion(sesion)
    try:
        ultima = IndicadorDAO.buscar_ultimo("uf")
    except ErrorBaseDatos:
        ultima = None
    if ultima is not None and ultima.fecha == date.today().isoformat():
        return ultima, ORIGEN_BD, "UF de hoy ya guardada."
    return consultar_indicador(sesion, "uf")


def salario_en_uf(sesion, salario):
    """Devuelve (monto_en_uf, dato_uf, origen, mensaje); monto_en_uf es None si no hay UF disponible."""
    dato, origen, mensaje = uf_vigente(sesion)
    if dato is None:
        return None, None, None, mensaje
    return salario / dato.valor, dato, origen, mensaje
