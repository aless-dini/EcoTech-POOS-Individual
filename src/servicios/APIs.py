import math
from datetime import datetime, timezone
import requests

URL_BASE = "https://open.er-api.com/v6/latest/"


def obtener_datos(moneda):
    try:
        respuesta = requests.get(URL_BASE + moneda, timeout=(3, 5))
        respuesta.raise_for_status()
    except requests.exceptions.Timeout:
        raise ConnectionError("La API tardó demasiado en responder.")
    except requests.exceptions.HTTPError as error:
        raise ConnectionError(f"La API respondió con un error: {error}")
    except requests.exceptions.RequestException as error:
        raise ConnectionError(f"No se pudo conectar con la API: {error}")

    try:
        return respuesta.json()
    except ValueError:
        raise ValueError("La respuesta de la API no es un JSON válido.")


def extraer_primero(datos):
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    if datos.get("result") != "success":
        raise ValueError("La API no entregó los datos")

    tasas = datos.get("rates")

    if not isinstance(tasas, dict) or "CLP" not in tasas:
        raise ValueError("No hay valores disponibles.")

    valor = tasas["CLP"]
    

    if (
        type(valor) not in (int,
    float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError("Valor del indicador inválido")

    segundos = datos.get("time_last_update_unix")
    if type(segundos) is not int:
        raise ValueError("La respuesta no trae la fecha")
    fecha = datetime.fromtimestamp(segundos, tz=timezone.utc).strftime("%Y-%m-%d")

    return fecha, valor


def main():
    moneda = input("Moneda a consultar: ").strip().upper()

    if len(moneda) != 3 or not moneda.isalpha():
        print("Error: el código de moneda debe tener 3 letras, por ejemplo: 'USD'")
        return

    try:
        datos = obtener_datos(moneda)
        fecha, valor = extraer_primero(datos)
    except (ConnectionError, ValueError) as error:
        print(f"Error: {error}")
        return

    print(f"Fecha: {fecha[:10]}")
    print(f"Valor de 1 {moneda}: ${valor:,.2f} CLP")


if __name__ == "__main__":
    main()