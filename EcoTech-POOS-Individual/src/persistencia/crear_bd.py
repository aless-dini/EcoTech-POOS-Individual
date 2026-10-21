from persistencia.conexion import (abrir_conexion,obtener_motor )

def asegurar_correo_unico(cursor):
    # CREATE TABLE IF NOT EXISTS no modifica tablas que ya existen,
    # por eso la restricción UNIQUE del correo se agrega aparte si falta.
    if obtener_motor() == "sqlite":
        cursor.execute("SELECT 1 FROM sqlite_master WHERE type = 'index' AND name = 'uq_empleado_correo'")
    else:
        cursor.execute(
            """SELECT 1 FROM information_schema.TABLE_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = DATABASE() AND TABLE_NAME = 'empleado'
            AND CONSTRAINT_NAME = 'uq_empleado_correo'"""
        )
    if cursor.fetchone() is not None:
        return

    cursor.execute("SELECT correo FROM empleado GROUP BY correo HAVING COUNT(*) > 1")
    repetidos = [fila[0] for fila in cursor.fetchall()]
    if repetidos:
        print("No se pudo agregar la restricción UNIQUE al correo porque hay correos repetidos:")
        for correo in repetidos:
            print(f"  - {correo}")
        print("Corrija esos empleados y vuelva a iniciar el programa.")
        return

    if obtener_motor() == "sqlite":
        cursor.execute("CREATE UNIQUE INDEX uq_empleado_correo ON empleado (correo)")
    else:
        cursor.execute("ALTER TABLE empleado ADD CONSTRAINT uq_empleado_correo UNIQUE (correo)")

def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    if obtener_motor() == "sqlite":
        sentencias = [
            """CREATE TABLE IF NOT EXISTS departamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                id_gerente INTEGER,
                FOREIGN KEY (id_gerente) REFERENCES empleado(id)
            )""",
            """CREATE TABLE IF NOT EXISTS empleado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_departamento INTEGER,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                correo TEXT NOT NULL,
                salario INTEGER NOT NULL,
                inicioContrato TEXT NOT NULL,
                FOREIGN KEY (id_departamento) REFERENCES departamento(id)
            )""",
            """CREATE TABLE IF NOT EXISTS proyecto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                fechaInicio TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS empleado_proyecto (
                id_empleado INTEGER NOT NULL,
                id_proyecto INTEGER NOT NULL,
                PRIMARY KEY (id_empleado, id_proyecto),
                FOREIGN KEY (id_empleado) REFERENCES empleado(id),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id)
            )""",
            """CREATE TABLE IF NOT EXISTS registroTiempo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empleado INTEGER NOT NULL,
                id_proyecto INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                horasTrabajadas REAL NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id)
            )""",
            """CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empleado INTEGER,
                nombre TEXT NOT NULL,
                contraseña TEXT NOT NULL,
                rol TEXT NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id)
            )""",
        ]
    else:
        sentencias = [
            """CREATE TABLE IF NOT EXISTS departamento (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                id_gerente INT
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS empleado (
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_departamento INT,
                nombre VARCHAR(100) NOT NULL,
                direccion VARCHAR(100) NOT NULL,
                telefono INT NOT NULL,
                correo VARCHAR(100) NOT NULL,
                salario INT NOT NULL,
                inicioContrato VARCHAR(100) NOT NULL,
                CONSTRAINT uq_empleado_correo UNIQUE (correo),
                FOREIGN KEY (id_departamento) REFERENCES departamento(id)
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS proyecto (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                descripcion VARCHAR(100) NOT NULL,
                fechaInicio VARCHAR(100) NOT NULL
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS empleado_proyecto (
                id_empleado INT NOT NULL,
                id_proyecto INT NOT NULL,
                PRIMARY KEY (id_empleado, id_proyecto),
                FOREIGN KEY (id_empleado) REFERENCES empleado(id),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id)
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS registroTiempo (
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_empleado INT NOT NULL,
                id_proyecto INT NOT NULL,
                fecha VARCHAR(100) NOT NULL,
                horasTrabajadas DECIMAL(4,2) NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id)
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS usuario (
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_empleado INT,
                nombre VARCHAR(100) NOT NULL,
                contraseña VARCHAR(100) NOT NULL,
                rol VARCHAR (100) NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id)
            ) ENGINE=InnoDB""",
        ]

    for sql in sentencias:
        cursor.execute(sql)

    asegurar_correo_unico(cursor)

    if obtener_motor() != "sqlite":
        cursor.execute(
            """SELECT 1 FROM information_schema.TABLE_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = DATABASE() AND TABLE_NAME = 'departamento'
            AND CONSTRAINT_NAME = 'fk_gerente'"""
        )
        if cursor.fetchone() is None:
            cursor.execute(
                """ALTER TABLE departamento
                ADD CONSTRAINT fk_gerente
                FOREIGN KEY (id_gerente) REFERENCES empleado(id)"""
            )
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()
