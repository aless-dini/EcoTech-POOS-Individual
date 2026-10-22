class RegistroTiempo:
    def __init__(self, fecha: str, horas: float, id_empleado: int = None, id_proyecto: int = None, id = None):
        self.id = id
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto
        self.fecha = fecha
        self.horas = horas

    def mostrar_registro(self) -> str:
        return f"{self.fecha} - {self.horas}"

    def realizar_informe(self) -> str:
        return f"Informe de tiempo: {self.fecha} — {self.horas} horas trabajadas"

    def exportar_informe(self, ruta: str = "informe_tiempo.txt") -> None:
        with open(ruta, "a", encoding="utf-8") as archivo:
            archivo.write(self.realizar_informe() + "\n")
