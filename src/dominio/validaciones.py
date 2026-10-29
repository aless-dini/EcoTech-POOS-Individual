from datetime import datetime

FORMATO_FECHA = "%d-%m-%Y"
ANIO_MINIMO = 1900

SOLO_LETRAS = (lambda c: c.isalpha() or c == " ", "solo acepta letras y espacios")
LETRAS_Y_NUMEROS = (lambda c: c.isalnum() or c == " ", "solo acepta letras, números y espacios")


def validar_texto(valor, campo, maximo, minimo=1, caracteres=None):
    if not isinstance(valor, str):
        raise TypeError(f"{campo} debe ser texto.")
    texto = " ".join(valor.split())
    if not minimo <= len(texto) <= maximo:
        raise ValueError(f"{campo} debe tener entre {minimo} y {maximo} caracteres.")
    if caracteres is not None:
        es_valido, aviso = caracteres
        if not all(es_valido(c) for c in texto):
            raise ValueError(f"{campo} {aviso}.")
    return texto


def a_fecha(texto):
    return datetime.strptime(texto, FORMATO_FECHA).date()


def validar_fecha(valor, campo):
    if not isinstance(valor, str):
        raise TypeError(f"{campo} debe ser texto.")
    try:
        fecha = a_fecha(valor.strip())
    except ValueError:
        raise ValueError(f"{campo} debe tener el formato DD-MM-AAAA (ejemplo: 15-03-2024).") from None
    if fecha.year < ANIO_MINIMO:
        raise ValueError(f"{campo} debe ser posterior al año {ANIO_MINIMO}.")
    return fecha.strftime(FORMATO_FECHA)


def validar_id_opcional(valor, campo):
    if valor is None:
        return None
    if type(valor) is not int or valor <= 0:
        raise ValueError(f"{campo} debe ser un número entero positivo.")
    return valor
