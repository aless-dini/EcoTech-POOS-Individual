# EcoTech Solutions – Sistema de Gestión de Empleados

Aplicación de consola en Python para gestionar los empleados, departamentos, proyectos, registros de horas y usuarios de EcoTech Solutions. Está hecha con programación orientada a objetos y guarda los datos en una base de datos SQLite o MySQL.

Proyecto de la asignatura **Programación Orientada a Objeto Seguro (TI3021)**.

## Requisitos

- Python 3.10 o superior
- Para usar MySQL: un servidor MySQL con una base de datos creada (las tablas las crea el programa)

## Dependencias

Todas están en `requirements.txt` y se instalan con un solo comando (ver Instalación):

| Librería | Para qué se usa |
|---|---|
| `bcrypt` | Cifrado y verificación de contraseñas |
| `PyMySQL` | Conexión a MySQL |
| `python-dotenv` | Lectura de la configuración desde el archivo `.env` |
| `requests` | Consultas HTTPS a APIs externas (`src/servicios/APIs.py`) |

`certifi`, `charset-normalizer`, `idna` y `urllib3` vienen como dependencias de `requests`.

## Instalación

```bash
git clone https://github.com/aless-dini/EcoTech-POOS-Individual.git
cd EcoTech-POOS-Individual
python -m venv .venv
source .venv/Scripts/activate      # Git Bash en Windows
# .venv\Scripts\activate           # CMD o PowerShell
pip install -r requirements.txt
```

> Si al ejecutar aparece `ModuleNotFoundError`, falta activar el entorno virtual o instalar las dependencias con `pip install -r requirements.txt`.

## Configuración

Copiar el archivo de ejemplo y completar los valores:

```bash
cp .env.example .env
```

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DB_ENGINE` | Motor de base de datos: `sqlite` o `mysql` | `sqlite` |
| `DB_NAME` | En SQLite, el archivo; en MySQL, el nombre de la base | `ecotech.db` |
| `DB_HOST` | Servidor MySQL | `localhost` |
| `DB_PORT` | Puerto MySQL | `3306` |
| `DB_USER` | Usuario MySQL | `root` |
| `DB_PASSWORD` | Contraseña MySQL | |
| `ADMIN_PASSWORD` | Contraseña de la cuenta `admin` que se crea al primer inicio (mínimo 8 caracteres). Si se deja vacía, `admin` se crea sin contraseña | |

Si no hay `.env`, el programa usa SQLite con el archivo `ecotech.db`, y sin `ADMIN_PASSWORD` la cuenta `admin` se crea sin contraseña: basta con presionar Enter al pedirla y luego cambiarla desde el menú de usuarios.

> Las credenciales van solo en el `.env`, que está en el `.gitignore` y nunca se sube al repositorio. El archivo `.env.example` sí se sube, sin valores secretos.

## Ejecución

Desde la raíz del proyecto:

```bash
python src/main.py
```

Al iniciar, el programa crea las tablas que falten y la cuenta `admin` si todavía no existe. Luego pide iniciar sesión. Si no logra conectarse a la base de datos, muestra un mensaje y se cierra sin errores. Los detalles técnicos de cualquier error quedan en `ecotech.log` (ignorado por git).

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
├── main.py              Punto de entrada: prepara la base, pide login y abre el menú principal
├── entradas.py          Funciones comunes para pedir un dato hasta que sea válido
├── dominio/             Clases del modelo UML (validan sus propios datos con @property)
│   ├── validaciones.py  Reglas comunes: largo de textos, fechas, ids
│   ├── empleado.py
│   ├── departamento.py
│   ├── proyecto.py
│   ├── registroTiempo.py
│   └── usuario.py
├── servicios/           Reglas de negocio
│   ├── autenticacion.py Registro, login y cambio de contraseña con bcrypt
│   ├── registros.py     Reglas de las horas: fecha, inicio del proyecto, máximo 24 h por día
│   └── APIs.py          Consumo de una API por HTTPS con requests
├── persistencia/        Acceso a la base de datos
│   ├── conexion.py      Conexión a SQLite o MySQL según el .env
│   ├── errores.py       ErrorBaseDatos: traduce los errores técnicos a mensajes claros
│   ├── crear_bd.py      Creación de las tablas
│   ├── semilla_bd.py    Datos iniciales y cuenta admin
│   ├── base_dao.py      Clase base con la lógica común de todos los DAO
│   └── *_dao.py         Un DAO por clase del dominio
└── menus/               Interacción con el usuario
    ├── menuPrincipal.py
    └── menu*.py         Un menú por entidad
docs/
├── uml_grupal.png       Diagrama de clases
└── uso_IA.md            Uso de herramientas de IA y decisiones técnicas
```

El programa está separado en capas:

- **Menús** (presentación): piden los datos y muestran resultados y mensajes. No contienen reglas.
- **Dominio**: cada clase protege sus atributos con `@property`; un objeto con datos inválidos no se puede crear ni modificar.
- **Servicios**: reglas que involucran varias entidades (por ejemplo, que un empleado no supere 24 horas en un día).
- **Persistencia**: guarda en la base de datos y convierte los errores técnicos en `ErrorBaseDatos`, que los menús muestran con un mensaje claro.

## Seguridad y manejo de errores

- **Consultas parametrizadas**: los datos del usuario nunca se insertan en el texto SQL, lo que evita la inyección SQL.
- **Contraseñas cifradas** con `bcrypt` (sal aleatoria incluida en el hash), con un máximo de 72 bytes por contraseña.
- **Contraseña oculta** al escribirla en la terminal (`getpass`).
- **Control de acceso por rol**: hay que iniciar sesión, y las acciones de administración quedan reservadas al rol `administrador`.
- **Validación de entradas**: cada dato se vuelve a pedir hasta que sea válido. Textos con largo mínimo y máximo (según las columnas de la base), correo, teléfono de 8 o 9 dígitos, salario entre 100.000 y 50.000.000, fechas reales y horas entre 0 y 24.
- **Reglas de negocio**: no se registran horas en fechas futuras ni antes del inicio del proyecto, un empleado no puede superar 24 horas en un mismo día, solo se registran horas en proyectos asignados y no se repiten nombres de departamento.
- **Errores de base de datos**: `BaseDAO` los convierte en `ErrorBaseDatos` con un mensaje que distingue la causa (sin conexión, dato repetido o relacionado, dato demasiado grande). El detalle técnico queda en `ecotech.log`, no en pantalla, y el programa sigue funcionando.
- **Integridad de los datos**: no se puede eliminar un empleado o proyecto con horas registradas, ni un departamento con empleados.
- **Peticiones HTTPS con timeout** y manejo de errores de conexión en las consultas con `requests`.

## Base de datos

Tablas: `departamento`, `empleado`, `proyecto`, `empleado_proyecto` (relación muchos a muchos entre empleados y proyectos), `registroTiempo` y `usuario`.

## Para trabajar en el proyecto

1. `git pull` antes de empezar.
2. Activar el entorno virtual (`source .venv/Scripts/activate`).
3. Si se instala una librería nueva, actualizar `requirements.txt` con `pip freeze > requirements.txt`.
4. Si se agrega una variable de configuración nueva, agregarla también a `.env.example`.
