import logging
import math
import os
from datetime import date
import requests
from dotenv import load_dotenv

load_dotenv()
registro = logging.getLogger("ecotech.api")

URL_BASE = "https://api.cmfchile.cl/api-sbifv3/recursos_api/"
FUENTE = "api.cmfchile.cl"
TIEMPO_ESPERA = (5, 15)

# Indicadores que el menú ofrece: código -> (nombre, unidad del valor, lista en la respuesta JSON).
INDICADORES = {
    "uf": ("Unidad de fomento (UF)", "CLP/UF", "UFs"),
    "utm": ("Unidad tributaria mensual (UTM)", "CLP/UTM", "UTMs"),
    "dolar": ("Dólar observado", "CLP/USD", "Dolares"),
}


def validar_codigo(codigo):
    if not isinstance(codigo, str) or codigo.strip().lower() not in INDICADORES:
        raise ValueError(f"Indicador no admitido. Use uno de estos: {', '.join(INDICADORES)}.")
    return codigo.strip().lower()


def obtener_datos(codigo):
    codigo = validar_codigo(codigo)
    clave = os.getenv("CMF_API_KEY")
    if not clave:
        raise ConnectionError("Falta CMF_API_KEY en el archivo .env.")

    # La clave va como parámetro y nunca se escribe en el log: los mensajes de error de
    # requests incluyen la URL completa, por eso solo se registra el tipo de error.
    try:
        respuesta = requests.get(URL_BASE + codigo, params={"apikey": clave, "formato": "json"},
                                 timeout=TIEMPO_ESPERA)
    except requests.exceptions.Timeout:
        registro.warning("Tiempo agotado al consultar %s", codigo)
        raise ConnectionError("La API tardó demasiado en responder.") from None
    except requests.exceptions.RequestException as error:
        registro.warning("Sin conexión al consultar %s (%s)", codigo, type(error).__name__)
        raise ConnectionError("No se pudo conectar con la API.") from None

    if respuesta.status_code != 200:
        # La CMF suele explicar el error en JSON, por ejemplo {"CodigoHTTP": 421, "Mensaje": "API key no valida"};
        # a veces responde una página HTML, y entonces no hay detalle.
        try:
            mensaje = respuesta.json().get("Mensaje", "sin detalle")
        except (ValueError, AttributeError):
            mensaje = "sin detalle"
        registro.warning("La API respondió %s al consultar %s: %s", respuesta.status_code, codigo, mensaje)
        raise ConnectionError(f"La API respondió con un error ({respuesta.status_code}): {mensaje}.")

    try:
        return respuesta.json()
    except ValueError:
        raise ValueError("La respuesta de la API no es un JSON válido.") from None


def codigo_de(datos):
    # La respuesta no trae el código: se deduce de la lista que contiene ("UFs" -> "uf").
    if isinstance(datos, dict):
        for codigo, (_, _, lista) in INDICADORES.items():
            if lista in datos:
                return codigo
    raise ValueError("La respuesta no corresponde a un indicador admitido.")


def a_numero(texto):
    # La CMF entrega los valores como texto en formato chileno: "39.485,65".
    try:
        return float(texto.replace(".", "").replace(",", "."))
    except (AttributeError, ValueError):
        raise ValueError("Valor del indicador inválido.") from None


def extraer_primero(datos):
    # La API entrega, por ejemplo, {"UFs": [{"Valor": "39.485,65", "Fecha": "2026-11-05"}]}.
    _, _, lista = INDICADORES[codigo_de(datos)]
    serie = datos[lista]
    if not isinstance(serie, list) or not serie or not isinstance(serie[0], dict):
        raise ValueError("La API no entregó valores.")

    valor = a_numero(serie[0].get("Valor"))
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError("Valor del indicador inválido.")

    try:
        fecha = date.fromisoformat(serie[0].get("Fecha")).isoformat()
    except (TypeError, ValueError):
        raise ValueError("La fecha de la respuesta no es válida.") from None

    return fecha, valor
