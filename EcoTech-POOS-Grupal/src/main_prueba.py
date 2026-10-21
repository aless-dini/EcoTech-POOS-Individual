import math
import requests

URL_DOLAR = "https://mindicador.cl/api/dolar"


def obtener_datos():
    # Consultar la API y devolver la respuesta como diccionario.
    try:
        respuesta = requests.get(URL_DOLAR, timeout=(3, 5))
        respuesta.raise_for_status()
    except requests.exceptions.Timeout:
        raise ConnectionError("La API tardó demasiado en responder.")
    except requests.exceptions.HTTPError as error:
        raise ConnectionError(f"La API respondió con un error: {error}")
    except requests.exceptions.RequestException as error:
        raise ConnectionError(f"No se pudo conectar con la API: {error}")

    # Convertir el texto de la respuesta a JSON.
    try:
        return respuesta.json()
    except ValueError:
        raise ValueError("La respuesta de la API no es un JSON válido.")


def extraer_primero(datos):
    # Verificar que la respuesta sea un diccionario.
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    # Obtener la lista de registros del indicador.
    serie = datos.get("serie")

    # Comprobar que sea una lista y contenga registros.
    if not isinstance(serie, list) or not serie:
        raise ValueError("No hay valores disponibles.")

    # Seleccionar el primer registro y obtener su valor.
    registro = serie[0]
    if not isinstance(registro, dict) or "valor" not in registro or "fecha" not in registro:
        raise ValueError("El registro no tiene fecha o valor.")
    valor = registro["valor"]

    # Aceptar solo números finitos y mayores que cero.
    if (
        type(valor) not in (int, float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError("Valor del indicador inválido.")

    # Devolver la fecha y el valor como una tupla.
    return registro["fecha"], valor


def main():
    try:
        datos = obtener_datos()
        fecha, valor = extraer_primero(datos)
    except (ConnectionError, ValueError) as error:
        print(f"Error: {error}")
        return

    # Mostrar solo la fecha (AAAA-MM-DD) y el valor en pesos chilenos.
    print(f"Fecha: {fecha[:10]}")
    print(f"Valor del dólar: ${valor:,.2f} CLP")


if __name__ == "__main__":
    main()