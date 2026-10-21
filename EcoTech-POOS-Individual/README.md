# EcoTech Solutions – Sistema de Gestión de Empleados

Aplicación de consola en Python para gestionar los empleados, departamentos, proyectos, registros de horas y usuarios de EcoTech Solutions. Está hecha con programación orientada a objetos y guarda los datos en una base de datos SQLite o MySQL.

Proyecto grupal de la asignatura **Programación Orientada a Objeto Seguro (TI3021)**.

## Requisitos

- Python 3.10 o superior
- Para usar MySQL: un servidor MySQL con una base de datos creada (las tablas las crea el programa)

## Instalación

```bash
git clone https://github.com/aless-dini/EcoTech-POOS-Grupal.git
cd EcoTech-POOS-Grupal
python -m venv .venv
source .venv/Scripts/activate      # Git Bash en Windows
# .venv\Scripts\activate           # CMD o PowerShell
pip install -r requirements.txt
```

## Configuración

La conexión se configura en el archivo `.env` de la raíz del proyecto:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DB_ENGINE` | Motor de base de datos: `sqlite` o `mysql` | `sqlite` |
| `DB_NAME` | En SQLite, el archivo; en MySQL, el nombre de la base | `ecotech.db` |
| `DB_HOST` | Servidor MySQL | `localhost` |
| `DB_PORT` | Puerto MySQL | `3306` |
| `DB_USER` | Usuario MySQL | `root` |
| `DB_PASSWORD` | Contraseña MySQL | |

Si no hay `.env`, el programa usa SQLite con el archivo `ecotech.db`.

> Las credenciales van solo en el `.env` y nunca en el código.

## Ejecución

Desde la raíz del proyecto:

```bash
python src/main.py
```

Al iniciar, el programa crea las tablas que falten. Si no logra conectarse a la base de datos, muestra un mensaje y se cierra sin errores.

**Si se cambia la estructura de las tablas**, hay que borrar la base y dejar que el programa la vuelva a crear (en SQLite, borrar `ecotech.db`), porque `CREATE TABLE IF NOT EXISTS` no modifica tablas que ya existen.

## Funcionalidades

| Menú | Opciones |
|---|---|
| Empleados | Registrar, actualizar, eliminar, listar, listar por departamento, buscar por id y por nombre |
| Departamentos | Crear, editar (nombre y gerente), eliminar, agregar y quitar empleados, listar empleados, ver cantidad |
| Proyectos | Crear, editar, eliminar, listar, buscar por id, asignar y quitar empleados, listar empleados |
| Registros de tiempo | Registrar horas, editar, eliminar, listar (todos, por empleado, por proyecto) con totales, exportar informe a `.txt` |
| Usuarios | Registrar, iniciar sesión, cambiar contraseña, editar rol y empleado asociado, eliminar, listar |

## Estructura del proyecto

```
src/
├── main.py              Punto de entrada: prepara la base y abre el menú principal
├── dominio/             Clases del modelo UML
│   ├── empleado.py
│   ├── departamento.py
│   ├── proyecto.py
│   ├── registroTiempo.py
│   ├── usuario.py
│   └── controlAcceso.py Cifrado y validación de contraseñas
├── persistencia/        Acceso a la base de datos
│   ├── conexion.py      Conexión a SQLite o MySQL según el .env
│   ├── crear_bd.py      Creación de las tablas
│   ├── base_dao.py      Clase base con la lógica común de todos los DAO
│   └── *_dao.py         Un DAO por clase del dominio
└── menus/               Interacción con el usuario y validación de entradas
    ├── menuPrincipal.py
    └── menu*.py         Un menú por entidad
docs/
└── uml_grupal.png       Diagrama de clases
```

El programa está separado en tres capas: los **menús** piden y validan los datos, el **dominio** representa las entidades y la **persistencia** las guarda en la base de datos.

## Seguridad y manejo de errores

- **Consultas parametrizadas**: los datos del usuario nunca se insertan en el texto SQL, lo que evita la inyección SQL.
- **Contraseñas cifradas** con PBKDF2-SHA256, una sal aleatoria y 100.000 iteraciones. La comparación usa `hmac.compare_digest`.
- **Contraseña oculta** al escribirla en la terminal (`getpass`).
- **Validación de entradas**: cada dato se vuelve a pedir hasta que sea válido (números, correo, teléfono, fechas reales, horas entre 0 y 24).
- **Errores de base de datos** capturados en `BaseDAO`: el programa informa el error y sigue funcionando.
- **Integridad de los datos**: no se puede eliminar un empleado o proyecto con horas registradas, ni un departamento con empleados.

## Base de datos

Tablas: `departamento`, `empleado`, `proyecto`, `empleado_proyecto` (relación muchos a muchos entre empleados y proyectos), `registroTiempo` y `usuario`.

## Para trabajar en el proyecto

1. `git pull` antes de empezar.
2. Activar el entorno virtual (`source .venv/Scripts/activate`).
3. Si se instala una librería nueva, actualizar `requirements.txt` con `pip freeze > requirements.txt`.
